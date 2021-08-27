# -*- coding: utf-8 -*-
"""Cheikh Tidiane Diop_ Image to Image Translation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1BrpBf7S_OD29kTfMBMV7nlzHeE9MmkNV
"""

import torch
import torch.nn as nn
class Discriminator(nn.Module):

  def __init__(self):
    super().__init__()
    self.l1= nn.Sequential(
        nn.Conv2d(3*2, 64, 4, 2, 1, padding_mode='reflect'),
        nn.LeakyReLU(0.2)
    )
    self.l2 = nn.Sequential(
        nn.Conv2d(64, 128, 4, 2, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(128),
        nn.LeakyReLU(0.2)
    )

    self.l3 = nn.Sequential(
        nn.Conv2d(128, 256, 4, 2, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(256),
        nn.LeakyReLU(0.2)
    )

    self.l4 = nn.Sequential(
        nn.Conv2d(256, 512, 4, 1, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(512),
        nn.LeakyReLU(0.2)
    )

    self.l5=nn.Sequential(
        nn.Conv2d(512, 1, 4, 1, 1, padding_mode='reflect')
    )


  def forward(self, input, generator_output):
    input_disc = torch.cat([input, generator_output], dim=1)
    return self.l5(self.l4(self.l3(self.l2(self.l1(input_disc)))))

x=torch.randn(1,3,286,286)
y=torch.randn(1,3,286,286)
m=Discriminator()
a =m(x,y)
a.shape

class Generator(nn.Module):

  def __init__(self):
    super().__init__()
    #Encoder Part
    self.l1= nn.Sequential(
        nn.Conv2d(3, 64, 4, 2, 1, padding_mode='reflect'),
        nn.LeakyReLU(0.2)
    )
    self.l2 = nn.Sequential(
        nn.Conv2d(64, 128, 4, 2, 1, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(128),
        nn.LeakyReLU(0.2)
    )

    self.l3 = nn.Sequential(
        nn.Conv2d(128, 256, 4, 2, 1, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(256),
        nn.LeakyReLU(0.2)
    )

    self.l4 = nn.Sequential(
        nn.Conv2d(256, 512, 4, 2, 1, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(512),
        nn.LeakyReLU(0.2)
    )

    self.l5 = nn.Sequential(
        nn.Conv2d(512, 512, 4, 2, 1, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(512),
        nn.LeakyReLU(0.2)
    )

    self.l6 = nn.Sequential(
        nn.Conv2d(512, 512, 4, 2, 1, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(512),
        nn.LeakyReLU(0.2)
    )

    self.l7 = nn.Sequential(
        nn.Conv2d(512, 512, 4, 2, 1, bias=False, padding_mode='reflect'),
        nn.BatchNorm2d(512),
        nn.LeakyReLU(0.2)
    )



    self.bottleneck=nn.Sequential(
        nn.Conv2d(512, 512, 4, 2, 1, padding_mode='reflect'),
        nn.ReLU()
    )

    #Decoder Part
    self.l8=nn.Sequential(
        nn.ConvTranspose2d(512, 512, 4, 2, 1, bias=False),
        nn.BatchNorm2d(512),
        nn.ReLU(),
        nn.Dropout(0.5)
    )

    self.l9=nn.Sequential(
        nn.ConvTranspose2d(1024, 512, 4, 2, 1, bias=False),
        nn.BatchNorm2d(512),
        nn.ReLU(),
        nn.Dropout(0.5)
    )
    

    self.l10=nn.Sequential(
        nn.ConvTranspose2d(1024, 512, 4, 2, 1, bias=False),
        nn.BatchNorm2d(512),
        nn.ReLU(),
        nn.Dropout(0.5)
    )

    self.l11=nn.Sequential(
        nn.ConvTranspose2d(1024, 512, 4, 2, 1, bias=False),
        nn.BatchNorm2d(512),
        nn.ReLU()
    )

    self.l12=nn.Sequential(
        nn.ConvTranspose2d(1024, 256, 4, 2, 1, bias=False),
        nn.BatchNorm2d(256),
        nn.ReLU()
    )

    self.l13=nn.Sequential(
        nn.ConvTranspose2d(512, 128, 4, 2, 1, bias=False),
        nn.BatchNorm2d(128),
        nn.ReLU()
    )

    self.l14=nn.Sequential(
        nn.ConvTranspose2d(256, 64, 4, 2, 1, bias=False),
        nn.BatchNorm2d(64),
        nn.ReLU()
    )

    self.l15=nn.Sequential(
        nn.ConvTranspose2d(128, 3, 4, 2, 1),
        nn.Tanh()
    )
    
  def forward(self, input):
    encoder1 = self.l1(input)
    encoder2 = self.l2(encoder1)
    encoder3 = self.l3(encoder2)
    encoder4 = self.l4(encoder3)
    encoder5 = self.l5(encoder4)
    encoder6 = self.l6(encoder5)
    encoder7 = self.l7(encoder6)
    bottleneck = self.bottleneck(encoder7)
    decoder1 = self.l8(bottleneck)
    decoder2 = self.l9(torch.cat([decoder1,encoder7], dim=1))
    decoder3 = self.l10(torch.cat([decoder2,encoder6], dim=1))
    decoder4 = self.l11(torch.cat([decoder3,encoder5], dim=1))
    decoder5 = self.l12(torch.cat([decoder4,encoder4], dim=1))
    decoder6 = self.l13(torch.cat([decoder5,encoder3], dim=1))
    decoder7 = self.l14(torch.cat([decoder6,encoder2], dim=1))
    output = self.l15(torch.cat([decoder7,encoder1], dim=1))
    return output

x = torch.randn((1,3,256,256))
gen = Generator()
pred = gen(x)

pred.shape

import torch
from torch import nn
from tqdm.auto import tqdm
from torchvision import transforms
from torchvision.utils import make_grid
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
torch.manual_seed(0)

def show_tensor_images(image_tensor, num_images=25, size=(1, 512, 256)):
    '''
    Function for visualizing images: Given a tensor of images, number of images, and
    size per image, plots and prints the images in an uniform grid.
    '''
    image_shifted = image_tensor
    image_unflat = image_shifted.detach().cpu().view(-1, *size)
    image_grid = make_grid(image_unflat[:num_images], nrow=5)
    plt.imshow(image_grid.permute(1, 2, 0).squeeze())
    plt.show()




def crop(image, new_shape):
    '''
    Function for cropping an image tensor: Given an image tensor and the new shape,
    crops to the center pixels.
    Parameters:
        image: image tensor of shape (batch size, channels, height, width)
        new_shape: a torch.Size object with the shape you want x to have
    '''
    middle_height = image.shape[2] // 2
    middle_width = image.shape[3] // 2
    starting_height = middle_height - round(new_shape[2] / 2)
    final_height = starting_height + new_shape[2]
    starting_width = middle_width - round(new_shape[3] / 2)
    final_width = starting_width + new_shape[3]
    cropped_image = image[:, :, starting_height:final_height, starting_width:final_width]
    return cropped_image

import torch.nn.functional as F
# New parameters
adv_criterion = nn.BCEWithLogitsLoss() 
recon_criterion = nn.L1Loss() 
lambda_recon = 200

n_epochs = 20
input_dim = 3
real_dim = 3
display_step = 200
batch_size = 4
lr = 0.0002
target_shape = 256
device = 'cuda'

from google.colab import drive
drive.mount('/content/Mydrive')

dataset_path="/content/Mydrive/MyDrive/cityscapes"

transform = transforms.Compose([
    transforms.ToTensor(),
])

import torchvision
dataset = torchvision.datasets.ImageFolder(dataset_path, transform=transform)

# UNQ_C2 (UNIQUE CELL IDENTIFIER, DO NOT EDIT)
# GRADED CLASS: get_gen_loss
def get_gen_loss(gen, disc, real, condition, adv_criterion, recon_criterion, lambda_recon):
    '''
    Return the loss of the generator given inputs.
    Parameters:
        gen: the generator; takes the condition and returns potential images
        disc: the discriminator; takes images and the condition and
          returns real/fake prediction matrices
        real: the real images (e.g. maps) to be used to evaluate the reconstruction
        condition: the source images (e.g. satellite imagery) which are used to produce the real images
        adv_criterion: the adversarial loss function; takes the discriminator 
                  predictions and the true labels and returns a adversarial 
                  loss (which you aim to minimize)
        recon_criterion: the reconstruction loss function; takes the generator 
                    outputs and the real images and returns a reconstructuion 
                    loss (which you aim to minimize)
        lambda_recon: the degree to which the reconstruction loss should be weighted in the sum
    '''
    # Steps: 1) Generate the fake images, based on the conditions.
    #        2) Evaluate the fake images and the condition with the discriminator.
    #        3) Calculate the adversarial and reconstruction losses.
    #        4) Add the two losses, weighting the reconstruction loss appropriately.
    #### START CODE HERE ####
    fake = gen(condition)
    disc_fake_bar = disc(fake, condition)
    gen_adv_loss = adv_criterion(disc_fake_bar, torch.ones_like(disc_fake_bar))
    gen_rec_loss = recon_criterion(real, fake)
    gen_loss_tot = gen_adv_loss + lambda_recon * gen_rec_loss
    #### END CODE HERE ####
    return gen_loss_tot

gen = Generator().to(device)
gen_opt = torch.optim.Adam(gen.parameters(), lr=lr)
disc = Discriminator().to(device)
disc_opt = torch.optim.Adam(disc.parameters(), lr=lr)

def weights_init(m):
    if isinstance(m, nn.Conv2d) or isinstance(m, nn.ConvTranspose2d):
        torch.nn.init.normal_(m.weight, 0.0, 0.02)
    if isinstance(m, nn.BatchNorm2d):
        torch.nn.init.normal_(m.weight, 0.0, 0.02)
        torch.nn.init.constant_(m.bias, 0)


gen = gen.apply(weights_init)
disc = disc.apply(weights_init)

from skimage import color
import numpy as np

def train(save_model=False):
    mean_generator_loss = 0
    mean_discriminator_loss = 0
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    cur_step = 0

    for epoch in range(n_epochs):
        # Dataloader returns the batches
        for image, _ in tqdm(dataloader):
            image_width = image.shape[3]
            condition = image[:, :, :, :image_width // 2]
            condition = nn.functional.interpolate(condition, size=target_shape)
            real = image[:, :, :, image_width // 2:]
            real = nn.functional.interpolate(real, size=target_shape)
            cur_batch_size = len(condition)
            condition = condition.to(device)
            real = real.to(device)

            ### Update discriminator ###
            disc_opt.zero_grad() # Zero out the gradient before backpropagation
            with torch.no_grad():
                fake = gen(condition)
            disc_fake_hat = disc(fake.detach(), condition) # Detach generator
            disc_fake_loss = adv_criterion(disc_fake_hat, torch.zeros_like(disc_fake_hat))
            disc_real_hat = disc(real, condition)
            disc_real_loss = adv_criterion(disc_real_hat, torch.ones_like(disc_real_hat))
            disc_loss = (disc_fake_loss + disc_real_loss) / 2
            disc_loss.backward(retain_graph=True) # Update gradients
            disc_opt.step() # Update optimizer

            ### Update generator ###
            gen_opt.zero_grad()
            gen_loss = get_gen_loss(gen, disc, real, condition, adv_criterion, recon_criterion, lambda_recon)
            gen_loss.backward() # Update gradients
            gen_opt.step() # Update optimizer

            # Keep track of the average discriminator loss
            mean_discriminator_loss += disc_loss.item() / display_step
            # Keep track of the average generator loss
            mean_generator_loss += gen_loss.item() / display_step

            ### Visualization code ###
            if cur_step % display_step == 0:
                if cur_step > 0:
                    print(f"Epoch {epoch}: Step {cur_step}: Generator (U-Net) loss: {mean_generator_loss}, Discriminator loss: {mean_discriminator_loss}")
                else:
                    print("Pretrained initial state")
                show_tensor_images(condition, size=(input_dim, target_shape, target_shape))
                show_tensor_images(real, size=(real_dim, target_shape, target_shape))
                show_tensor_images(fake, size=(real_dim, target_shape, target_shape))
                mean_generator_loss = 0
                mean_discriminator_loss = 0
                # You can change save_model to True if you'd like to save the model
                if save_model:
                    torch.save({'gen': gen.state_dict(),
                        'gen_opt': gen_opt.state_dict(),
                        'disc': disc.state_dict(),
                        'disc_opt': disc_opt.state_dict()
                    }, f"pix2pix_{cur_step}.pth")
            cur_step += 1
train()

