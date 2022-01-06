import PIL
import string
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from matplotlib import font_manager

GUESS_FONT_SIZE = 50
ALPHABET_FONT_SIZE = 28

VALID = (0, 255, 0)
IN_WORD = (255, 150, 0)
INVALID = (255, 0, 0)

USED_CORRECT = (100, 128, 100)
USED_INCORRECT = (128, 100, 100)
UNUSED = (255, 255, 255)

def generate_letters_image(guessed_letters, word):
    font_search = font_manager.FontProperties(family='sans-serif', weight='bold')
    font_file = font_manager.findfont(font_search)
    font = ImageFont.truetype(font_file, ALPHABET_FONT_SIZE)

    alphabet_string = string.ascii_uppercase

    req_width, req_height = font.getsize(alphabet_string)

    img=Image.new("RGBA", (req_width + 10, req_height))
    draw = ImageDraw.Draw(img)

    total_size = 0

    for l in alphabet_string:
        lwidth, lheight = font.getsize(l)

        if l in guessed_letters:
            if l in word:
                fill = USED_CORRECT
            else:
                fill = USED_INCORRECT
        else:
            fill = UNUSED

        draw.text((total_size, 0), l, fill=fill, font=font)

        total_size += lwidth

    img.save("letters_used.png")

def generate_guess_image(guess, word):
    font_search = font_manager.FontProperties(family='sans-serif', weight='bold')
    font_file = font_manager.findfont(font_search)
    font = ImageFont.truetype(font_file, GUESS_FONT_SIZE)

    required_size = font.getsize(guess)

    img=Image.new("RGBA", required_size)
    draw = ImageDraw.Draw(img)

    total_size = 0

    for i in range(0, len(guess)):
        letter = guess[i]
        lwidth, lheight = font.getsize(letter)

        if letter == word[i]:
            fill = VALID
        else:
            if letter in word:
                fill = IN_WORD
            else:
                fill = INVALID

        draw.text((total_size, 0), letter, fill=fill, font=font)

        total_size += lwidth


    img.save("guess_result.png")