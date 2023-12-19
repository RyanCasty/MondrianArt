import random
from PIL import Image, ImageDraw
import extcolors
import colorsys

class Mondrian:
  def __init__(self, w, h, image_or_color, box_width_percentage, line_width, image_slash_color_placeholder = None):
    self.image = Image.new("RGBA", (w,h), (255,255,255))
    self.box_width_percentage = box_width_percentage
    self.line_width = line_width
    
    if image_or_color.lower() == "image":
      self.color_list = self.create_color_palette(image_slash_color_placeholder)
      
    elif image_or_color.lower() == "color":
      
      if image_slash_color_placeholder == None:
        
        color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
        
        self.color_list = self.color_gen(colorsys.rgb_to_hsv(color[0]/255.0,color[1]/255.0,color[2]/255.0))
        
      else:
        self.color_list = self.color_gen(colorsys.rgb_to_hsv(image_slash_color_placeholder[0]/255.0,image_slash_color_placeholder[1]/255.0,image_slash_color_placeholder[2]/255.0))
        print(self.color_list)
      
    self.mondrian_generation(self.random_point((0,0,self.image.size[0], self.image.size[1]), self.image.size[0], self.image.size[1]))
    self.image.save("outfile.png")
    
  def random_point(self, box, box_w, box_h):

    randx = random.randrange(box[0] + int(box_w/3), box[2] - int(box_w/3))
    randy = random.randrange(box[1] + int(box_h/3), box[3] - int(box_h/3))
    return [(box[0], box[1], randx, randy), (randx, box[1], box[2], randy), (randx, randy, box[2], box[3]), (box[0], randy, randx, box[3])]

  def mondrian_generation(self, box_list):

    for box in box_list:
      box_w = box[2]-box[0]
      box_h = box[3]-box[1]
      divisor = self.box_width_percentage

      if box_w <= self.image.size[0]/divisor or box_h <= self.image.size[1]/divisor:
        img1 = ImageDraw.Draw(self.image)
        img1.rectangle(box, random.choice(self.color_list), outline = "black", width = self.line_width)
      
      else:
        new_box_list = self.random_point(box, box_w, box_h)
        self.mondrian_generation(new_box_list)

    return self.image
   
  def color_gen(self, hsv):
    color_list = [colorsys.hsv_to_rgb(hsv[0] % 1.0, hsv[1], hsv[2])]

    # Calculate the two additional hues for a triad color palette
    hue1 = (hsv[0] + 1/3) % 1.0
    hue2 = (hsv[0] + 2/3) % 1.0

    color_list.append(colorsys.hsv_to_rgb(hue1, hsv[1], hsv[2]))
    color_list.append(colorsys.hsv_to_rgb(hue2, hsv[1], hsv[2]))

    return [(int(r * 255), int(g * 255), int(b * 255)) for r, g, b in color_list]


    
  def create_color_palette(self, image):
    colors_x = extcolors.extract_from_path(self.resize(image), tolerance = 25, limit = 10)
    tups = colors_x[0]
    color_list = []
    
    for mega in tups:
      color_list.append(mega[0])
  
    return color_list

  def resize(self, image):
    input_name = image
    output_width = 50

    img = Image.open(input_name)
    wpercent = (output_width/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((output_width,hsize), Image.Resampling.LANCZOS)
    
    resize_name = 'resize_.jpg'
    img.save(resize_name) 
    return resize_name
    
m = Mondrian(900, 600, "Color", 5, 10)