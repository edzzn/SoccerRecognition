from __future__ import division
import cv2
import numpy as np
from PIL import Image

import time
import torch
import torch.nn as nn
from torch.autograd import Variable
from util import *
import argparse
import os
import os.path as osp
from darknet import Darknet
import pickle as pkl
import pandas as pd
import random

from reconocer_equipos import reconocer_equipo
from reconocer_numeros import reconocer_numero
from ball_speed import Ball, write_ball_speed
from lineas_gol import LineasGol
from reconocimiento_facial.reconocimiento_facial import ReconocimientoFacial

batch_size = 1
confidence = 0.3
nms_thesh = 0.4
resolution = 416
start = 0
CUDA = torch.cuda.is_available()
player_counter = 0
weightsfile = 'yolov3.weights'
cfgfile = 'cfg/yolov3.cfg'

num_classes = 80
# classes = load_classes("data/coco.names")
classes = load_classes('data/coco.names')
colors = pkl.load(open("pallete", "rb"))

ball = Ball()
lineaGol = LineasGol()
ball_speed = 0


class Detector:
    def __init__(self, showTags=False, showCordenates=False):
        self.showTags = showTags
        self.showCordenates = showCordenates

        self.model = Darknet(cfgfile)
        self.model.load_weights(weightsfile)
        self.model.net_info["height"] = resolution
        self.inp_dim = int(self.model.net_info["height"])
        assert self.inp_dim % 32 == 0
        assert self.inp_dim > 32

        # If there's a GPU availible, put the model on GPU
        if CUDA:
            self.model.cuda()

        self.model.eval()
        self.reconocimiento_facil = ReconocimientoFacial()

    def detect(self, frame, debugFrames=[], frame_counter=0):

        img = prep_image(frame, self.inp_dim)

        im_dim = frame.shape[1], frame.shape[0]
        im_dim = torch.FloatTensor(im_dim).repeat(1, 2)

        if CUDA:
            im_dim = im_dim.cuda()
            img = img.cuda()

        with torch.no_grad():
            # output = self.model(Variable(img, volatile=True), CUDA)
            output = self.model(Variable(img), CUDA)
        output = write_results(
            output, confidence, num_classes, nms_conf=nms_thesh)

        if isinstance(output, int):
            return frame

        im_dim = im_dim.repeat(output.size(0), 1)
        scaling_factor = torch.min(416/im_dim, 1)[0].view(-1, 1)

        output[:, [1, 3]] -= (self.inp_dim - scaling_factor *
                              im_dim[:, 0].view(-1, 1))/2
        output[:, [2, 4]] -= (self.inp_dim - scaling_factor *
                              im_dim[:, 1].view(-1, 1))/2

        output[:, 1:5] /= scaling_factor

        for i in range(output.shape[0]):
            output[i, [1, 3]] = torch.clamp(
                output[i, [1, 3]], 0.0, im_dim[i, 0])
            output[i, [2, 4]] = torch.clamp(
                output[i, [2, 4]], 0.0, im_dim[i, 1])

        if(self.showCordenates):
            frame = lineaGol.add_linea_gol(frame, frame_counter)

        list(map(lambda x: write(x, frame, self.showTags,
                                 self.reconocimiento_facil), output))

        return frame


def write(x, results, showTags, reconocimiento_facil):
    global ball
    global player_counter
    global ball_speed

    c1 = tuple(x[1:3].int())
    c2 = tuple(x[3:5].int())
    img = results
    cls = int(x[-1])
    # color = random.choice(colors)
    color = (255, 0, 0)
    label = "{0}".format(classes[cls])

    if (label == 'person' or label == 'sports ball'):
        label = 'Persona' if label == 'person' else 'Balon'

        if label == 'Balon':
            img, ball_speed = ball.draw(img, c1, c2, color)
        write_ball_speed(ball_speed, img)

        if label == 'Persona':
            # if abs(c1[0] - c2[0]) > 200:
            #     return img

            cropped_image = crop_iamge(img, c1, c2)
            # Saving cropped image
            # cv2.imwrite(f"./personas/j-{player_counter}.jpg", cropped_image)

            # player_counter += 1

            label, color = reconocer_equipo(cropped_image)
            if showTags:
                # numero = reconocer_numero(cropped_image)
                name = reconocimiento_facil.detect(cropped_image)
                if (name != '' and name != None):
                    label = f"{name} - {label}"

            cv2.rectangle(img, c1, c2, color, 1)

            t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_PLAIN, 1, 1)[0]
            c2 = c1[0] + t_size[0] + 3, c1[1] + t_size[1] + 4
            cv2.rectangle(img, c1, c2, color, -1)
            cv2.putText(img, label, (c1[0], c1[1] + t_size[1] + 4),
                        cv2.FONT_HERSHEY_PLAIN, 1, [225, 255, 255], 1)
    return img


def crop_iamge(img, c1, c2):
    return img[c1[1]:c2[1], c1[0]:c2[0]]
