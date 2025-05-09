from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

import math
import random
import time

# ======== GAME CONSTANTS ========
W_width = 1000
W_height = 800
grid_length = 600

# ======== GAME STATE CLASS ========
class GameState:
    def __init__(self):
        self.game_start_time = time.time()
        self.game_end_time = 0
        self.victory_achieved = False

        # Camera
        self.cam_pos = [0, 600, 600]
        self.cam_angle = 0
        self.cam_radius = 600
        self.cam_height = 600
        self.fovY = 120
        
        # Player
        self.p_pos = [0, 0, 0]
        self.p_angle = 0
        self.p_speed = 10
        self.p_turn_speed = 8
        self.p_life = 5
        self.p_score = 0
        self.p_coins = 0
        self.weapon_level = 1
        self.g_point = [30, 15, 80]
        self.player_radius = 20
        
        # Enemy
        self.e_list = []
        self.e_pulse = 1.0
        self.e_pulse_time = 0
        self.e_speed = 0.025
        self.e_size = 30
        self.wave = 1
        self.max_waves = 5
        self.boss_spawned = False
        self.boss_defeated = False
        
        # Gun
        self.g_bullets = []
        self.g_bullet_size = 7.5
        self.g_bullet_speed = 1
        self.max_bullets = 30
        self.current_bullets = 30
        
        # Collectibles
        self.coins = []
        self.coin_radius = 10
        self.chests = []
        self.chest_radius = 15
        self.diamonds = []
        self.diamond_radius = 12
        self.ammo_packs = []
        self.ammo_radius = 12
        self.last_spawn_time = time.time()
        self.spawn_interval = 5
        
        # Game Flags
        self.first_person = False
        self.cheat = False
        self.cheat_vision = False
        self.cheat_angle_margin = 0.05
        self.cheat_angle_margin_1st = self.cheat_angle_margin / 2
        self.over = False
        self.game_won = False

game = GameState()

# ======== DRAWING FUNCTIONS ========
def draw_cube(size=1.0):
    s = size / 2.0
    glBegin(GL_QUADS)
    # Front face
    glVertex3f(-s, -s, s)
    glVertex3f(s, -s, s)
    glVertex3f(s, s, s)
    glVertex3f(-s, s, s)
    # Back face
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, -s, -s)
    # Top face
    glVertex3f(-s, s, -s)
    glVertex3f(-s, s, s)
    glVertex3f(s, s, s)
    glVertex3f(s, s, -s)
    # Bottom face
    glVertex3f(-s, -s, -s)
    glVertex3f(s, -s, -s)
    glVertex3f(s, -s, s)
    glVertex3f(-s, -s, s)
    # Right face
    glVertex3f(s, -s, -s)
    glVertex3f(s, s, -s)
    glVertex3f(s, s, s)
    glVertex3f(s, -s, s)
    # Left face
    glVertex3f(-s, -s, -s)
    glVertex3f(-s, -s, s)
    glVertex3f(-s, s, s)
    glVertex3f(-s, s, -s)
    glEnd()

def draw_grid():
    glBegin(GL_QUADS)
    for i in range(-grid_length, grid_length + 1, 100):
        for j in range(-grid_length, grid_length + 1, 100):
            if (i + j) % 200 == 0:
                glColor3f(0, 0, 0)
            else:
                glColor3f(0.7, 0.5, 0.95)

            glVertex3f(i, j, 0)
            glVertex3f(i + 100, j, 0)
            glVertex3f(i + 100, j + 100, 0)
            glVertex3f(i, j + 100, 0)

    # Boundary walls
    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(-grid_length, -grid_length, 0)
    glVertex3f(-grid_length, grid_length+100, 0)
    glVertex3f(-grid_length, grid_length+100, 100)
    glVertex3f(-grid_length, -grid_length, 100)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(grid_length+100, -grid_length, 0)
    glVertex3f(grid_length+100, grid_length+100, 0)
    glVertex3f(grid_length+100, grid_length+100, 100)
    glVertex3f(grid_length+100, -grid_length, 100)

    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-grid_length, grid_length+100, 0)
    glVertex3f(grid_length+100, grid_length+100, 0)
    glVertex3f(grid_length+100, grid_length+100, 100)
    glVertex3f(-grid_length, grid_length+100, 100)

    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-grid_length, -grid_length, 0)
    glVertex3f(grid_length+100, -grid_length, 0)
    glVertex3f(grid_length+100, -grid_length, 100)
    glVertex3f(-grid_length, -grid_length, 100)
    glEnd()

def draw_player():
    glPushMatrix()
    glTranslatef(*game.p_pos)
    glRotatef(game.p_angle, 0, 0, 1)

    if game.over:
        glRotatef(-90, 1, 0, 0)

    # Head
    glPushMatrix()
    glTranslatef(0, 0, 70)
    glColor3f(0.8, 0.6, 0.4)  # Skin tone
    glutSolidSphere(15, 20, 20)
    
    # Face (front side)
    glPushMatrix()
    glRotatef(90, 1, 0, 0)
    glColor3f(0.8, 0.6, 0.4)  # Skin tone
    
    # Eyes
    glPushMatrix()
    glTranslatef(5, 10, 12)
    glColor3f(1, 1, 1)
    glutSolidSphere(3, 10, 10)
    glTranslatef(-10, 0, 0)
    glutSolidSphere(3, 10, 10)
    glPopMatrix()
    
    # Pupils
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(5, 10, 14)
    glutSolidSphere(1.5, 10, 10)
    glTranslatef(-10, 0, 0)
    glutSolidSphere(1.5, 10, 10)
    glPopMatrix()
    
    
    glPopMatrix()
    glPopMatrix()

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 40)
    
    # Front torso
    glColor3f(0, 0, 0.8)  # Blue armor
    glBegin(GL_QUADS)
    glVertex3f(-15, -15, 15)
    glVertex3f(15, -15, 15)
    glVertex3f(15, 15, 15)
    glVertex3f(-15, 15, 15)
    glEnd()
    
    # Back torso
    glColor3f(0, 0, 0.5)  # Darker blue
    glBegin(GL_QUADS)
    glVertex3f(-15, -15, -15)
    glVertex3f(-15, 15, -15)
    glVertex3f(15, 15, -15)
    glVertex3f(15, -15, -15)
    glEnd()
    
    # Sides
    glColor3f(0, 0, 0.6)
    glBegin(GL_QUAD_STRIP)
    glVertex3f(-15, -15, 15)
    glVertex3f(-15, -15, -15)
    glVertex3f(15, -15, 15)
    glVertex3f(15, -15, -15)
    glVertex3f(15, 15, 15)
    glVertex3f(15, 15, -15)
    glVertex3f(-15, 15, 15)
    glVertex3f(-15, 15, -15)
    glVertex3f(-15, -15, 15)
    glVertex3f(-15, -15, -15)
    glEnd()
    glPopMatrix()

    # Arms
    # Right arm
    glPushMatrix()
    glTranslatef(20, 0, 40)
    glRotatef(-45, 0, 1, 0)
    
    # Upper arm
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.2)
    glutSolidCube(20)
    glPopMatrix()
    
    # Elbow
    glTranslatef(0, 0, 12)
    glColor3f(0.8, 0.6, 0.4)
    glutSolidSphere(5, 10, 10)
    
    # Lower arm
    glTranslatef(0, 0, 12)
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.2)
    glutSolidCube(20)
    glPopMatrix()
    
    # Hand
    glTranslatef(0, 0, 12)
    glColor3f(0.8, 0.6, 0.4)
    glutSolidSphere(6, 10, 10)
    glPopMatrix()

    # Left arm (holding gun)
    glPushMatrix()
    glTranslatef(-20, 0, 40)
    glRotatef(45, 0, 1, 0)
    
    # Upper arm
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.2)
    glutSolidCube(20)
    glPopMatrix()
    
    # Elbow
    glTranslatef(0, 0, 12)
    glColor3f(0.8, 0.6, 0.4)
    glutSolidSphere(5, 10, 10)
    
    # Lower arm
    glTranslatef(0, 0, 12)
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.2)
    glutSolidCube(20)
    glPopMatrix()
    
    # Hand
    glTranslatef(0, 0, 12)
    glColor3f(0.8, 0.6, 0.4)
    glutSolidSphere(6, 10, 10)
    glPopMatrix()

    # Legs
    # Right leg
    glPushMatrix()
    glTranslatef(8, 0, 0)
    
    # Upper leg
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.5)
    glutSolidCube(20)
    glPopMatrix()
    
    # Knee
    glTranslatef(0, 0, -15)
    glColor3f(0.8, 0.6, 0.4)
    glutSolidSphere(5, 10, 10)
    
    # Lower leg
    glTranslatef(0, 0, -15)
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.5)
    glutSolidCube(20)
    glPopMatrix()
    
    # Foot
    glTranslatef(0, 0, -15)
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glScalef(1.2, 1.5, 0.5)
    glutSolidCube(15)
    glPopMatrix()
    glPopMatrix()

    # Left leg
    glPushMatrix()
    glTranslatef(-8, 0, 0)
    
    # Upper leg
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.5)
    glutSolidCube(20)
    glPopMatrix()
    
    # Knee
    glTranslatef(0, 0, -15)
    glColor3f(0.8, 0.6, 0.4)
    glutSolidSphere(5, 10, 10)
    
    # Lower leg
    glTranslatef(0, 0, -15)
    glColor3f(0, 0, 0.8)
    glPushMatrix()
    glScalef(0.7, 0.7, 1.5)
    glutSolidCube(20)
    glPopMatrix()
    
    # Foot
    glTranslatef(0, 0, -15)
    glColor3f(0.2, 0.2, 0.2)
    glPushMatrix()
    glScalef(1.2, 1.5, 0.5)
    glutSolidCube(15)
    glPopMatrix()
    glPopMatrix()

    # Gun (assault rifle)
    glPushMatrix()
    glTranslatef(-18, 5, 50)  # Position in hand
    glRotatef(90,1,0,0)
    
    
    # Barrel
    glTranslatef(0, 0, 20)
    gluCylinder(gluNewQuadric(), 2, 1.5, 30, 20, 20)
    
    # Scope
    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(3, 3, 10)
    glScalef(1.5, 1.5, 3)
    glutSolidCube(5)
    glPopMatrix()
    

    
    # Stock
    glColor3f(0.5, 0.3, 0.1)
    glPushMatrix()
    glTranslatef(0, 0, -15)
    glScalef(1.2, 1.5, 1.5)
    glutSolidCube(10)
    glPopMatrix()
    glPopMatrix()

    glPopMatrix()
    game.g_point = [30, 15, 80]

def draw_bullet(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.8, 0.5, 0.2)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 10, 10, 10)
    glTranslatef(0, 0, 10)
    glutSolidCone(2, 4, 10, 10)
    glTranslatef(0, 0, -10)
    glColor3f(0.5, 0.5, 0.5)
    glutSolidTorus(1, 2, 5, 10)
    glPopMatrix()

def draw_coin(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 0.84, 0)
    glRotatef(90, 1, 0, 0)
    glutSolidTorus(2, 8, 10, 20)
    glColor3f(0.9, 0.7, 0.1)
    glutSolidTorus(1, 6, 10, 20)
    glPopMatrix()

def draw_ammo(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.8, 0.5, 0.2)
    
    # Ammo clip
    glPushMatrix()
    glRotatef(45, 1, 1, 0)
    glScalef(0.8, 0.8, 1.5)
    glutSolidCube(10)
    glPopMatrix()
    
    # Bullets
    glColor3f(0.5, 0.5, 0.5)
    for i in range(3):
        glPushMatrix()
        glTranslatef(0, 0, i*3 - 3)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 1.5, 1.5, 3, 10, 10)
        glPopMatrix()
    glPopMatrix()

def draw_chest(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Main chest
    glColor3f(0.8, 0.6, 0.2)
    glPushMatrix()
    glScalef(1.5, 1.0, 1.0)
    glutSolidCube(25)
    glPopMatrix()
    
    # Lid
    glPushMatrix()
    glTranslatef(0, 0, 15)
    glRotatef(20, 1, 0, 0)
    glScalef(1.5, 1.0, 0.2)
    glutSolidCube(25)
    glPopMatrix()
    
    # Rubies
    glColor3f(1.0, 0.0, 0.0)
    for i in [-1, 1]:
        glPushMatrix()
        glTranslatef(i*10, 15, 5)
        glutSolidSphere(3, 10, 10)
        glPopMatrix()
    
    # Lock
    glColor3f(0.3, 0.3, 0.3)
    glPushMatrix()
    glTranslatef(0, 12, 5)
    glutSolidSphere(4, 10, 10)
    glPopMatrix()
    
    glPopMatrix()

def draw_diamond(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Diamond parameters
    size = 12
    height = 20
    top_height = height * 0.6
    bottom_height = height * 0.4
    
    top_apex = (0, 0, top_height)
    top_base = [
        (size, 0, 0),
        (0, size, 0),
        (-size, 0, 0),
        (0, -size, 0)
    ]
    
    bottom_nadir = (0, 0, -bottom_height)
    
    glColor3f(1.0, 0.5, 0.8)  # Base pink
    
    # Draw top pyramid
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(*top_apex)
    for point in top_base:
        glVertex3f(*point)
    glVertex3f(*top_base[0])  # Close the loop
    glEnd()
    
    #bottom pyramid
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(*bottom_nadir)
    for point in reversed(top_base):
        glVertex3f(*point)
    glVertex3f(*top_base[-1])  # Close the loop
    glEnd()
    
    #connecting quadrilaterals
    glBegin(GL_QUAD_STRIP)
    for i in range(len(top_base)):
        next_i = (i + 1) % len(top_base)
        glColor3f(1.0, 0.6, 0.9)  # Lighter pink
        glVertex3f(*top_base[i])
        glVertex3f(*top_base[next_i])
        glColor3f(1.0, 0.4, 0.7)  # Darker pink
        glVertex3f(*top_base[i])
        glVertex3f(*top_base[next_i])
    glEnd()
    
    
    # Vertical line
    glVertex3f(0, 0, top_height)
    glVertex3f(0, 0, -bottom_height)
    # Cross lines
    glVertex3f(size, 0, 0)
    glVertex3f(-size, 0, 0)
    glVertex3f(0, size, 0)
    glVertex3f(0, -size, 0)
    glEnd()
    glLineWidth(1.0)
    
    glPopMatrix()

def draw_collectibles():
    for coin in game.coins:
        draw_coin(*coin[:3])
    for ammo in game.ammo_packs:
        draw_ammo(*ammo[:3])
    for chest in game.chests:
        draw_chest(*chest[:3])
    for diamond in game.diamonds:
        draw_diamond(*diamond[:3])

def draw_enemy(x, y, z, hp=1, is_boss=False):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    is_boss = hp > 5
    scale = 1.5 if is_boss else 1.0
    color = (0.8, 0.1, 0.1) if is_boss else (0.7, 0.0, 0.0)
    
    # Head
    glPushMatrix()
    glTranslatef(0, 0, 60 * scale)
    glColor3f(*color)
    glutSolidSphere(15 * scale, 20, 20)
    
    # Eyes
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(5 * scale, 10 * scale, 12 * scale)
    glutSolidSphere(3 * scale, 10, 10)
    glTranslatef(-10 * scale, 0, 0)
    glutSolidSphere(3 * scale, 10, 10)
    glPopMatrix()
    
    # Eyebrows
    glColor3f(0.0, 0.0, 0.0)
    glBegin(GL_LINES)
    glVertex3f(3 * scale, 8 * scale, 12 * scale)
    glVertex3f(8 * scale, 13 * scale, 12 * scale)
    glVertex3f(-3 * scale, 8 * scale, 12 * scale)
    glVertex3f(-8 * scale, 13 * scale, 12 * scale)
    glEnd()
    
    # Mouth
    glBegin(GL_LINE_STRIP)
    glVertex3f(-8 * scale, 5 * scale, 12 * scale)
    glVertex3f(0, 0, 12 * scale)
    glVertex3f(8 * scale, 5 * scale, 12 * scale)
    glEnd()
    glPopMatrix()

    # Body
    glPushMatrix()
    glTranslatef(0, 0, 30 * scale)
    glColor3f(*color)
    glScalef(1.0, 0.8, 1.5)
    glutSolidCube(30 * scale)
    
    # Spikes
    glColor3f(0.5, 0.5, 0.5)
    for i in [-1, 1]:
        for j in [-1, 1]:
            glPushMatrix()
            glTranslatef(i*12*scale, j*8*scale, 15*scale)
            glutSolidCone(3*scale, 8*scale, 10, 10)
            glPopMatrix()
    glPopMatrix()

    # Arms
    # Right arm
    glPushMatrix()
    glTranslatef(20 * scale, 0, 30 * scale)
    glRotatef(-30, 0, 1, 0)
    glScalef(0.6, 0.6, 1.2)
    glutSolidCube(20 * scale)
    # Claw
    glTranslatef(0, 0, 15 * scale)
    glColor3f(0.3, 0.3, 0.3)
    for i in range(3):
        glPushMatrix()
        glRotatef(i*30-30, 0, 1, 0)
        glTranslatef(0, 0, 5 * scale)
        glutSolidCone(1.5*scale, 8*scale, 5, 5)
        glPopMatrix()
    glPopMatrix()
    
    # Left arm
    glPushMatrix()
    glTranslatef(-20 * scale, 0, 30 * scale)
    glRotatef(30, 0, 1, 0)
    glScalef(0.6, 0.6, 1.2)
    glutSolidCube(20 * scale)
    # Claw
    glTranslatef(0, 0, 15 * scale)
    glColor3f(0.3, 0.3, 0.3)
    for i in range(3):
        glPushMatrix()
        glRotatef(i*30-30, 0, 1, 0)
        glTranslatef(0, 0, 5 * scale)
        glutSolidCone(1.5*scale, 8*scale, 5, 5)
        glPopMatrix()
    glPopMatrix()

    # Legs
    # Right leg
    glPushMatrix()
    glTranslatef(10 * scale, 0, 0)
    glScalef(0.6, 0.6, 1.5)
    glutSolidCube(20 * scale)
    # Boot
    glTranslatef(0, 0, -15 * scale)
    glColor3f(0.2, 0.2, 0.2)
    glScalef(1.2, 1.5, 0.5)
    glutSolidCube(15 * scale)
    glPopMatrix()
    
    # Left leg
    glPushMatrix()
    glTranslatef(-10 * scale, 0, 0)
    glScalef(0.6, 0.6, 1.5)
    glutSolidCube(20 * scale)
    # Boot
    glTranslatef(0, 0, -15 * scale)
    glColor3f(0.2, 0.2, 0.2)
    glScalef(1.2, 1.5, 0.5)
    glutSolidCube(15 * scale)
    glPopMatrix()

    # HP display
    if hp > 1:
        glColor3f(1, 1, 1)
        glRasterPos2f(-5 * scale, 80 * scale)
        for char in str(hp):
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

    glPopMatrix()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, W_width, 0, W_height)

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

# ======== GAME LOGIC FUNCTIONS ========
def set_camera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(game.fovY, float(W_width)/float(W_height), 0.1, 1500)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if game.first_person:
        angle = math.radians(game.p_angle)
        eyeX = game.p_pos[0] + game.g_point[0]/2 * math.sin(angle) - game.g_point[1] * math.cos(angle)
        eyeY = game.p_pos[1] - game.g_point[0]/2 * math.cos(angle) - game.g_point[1] * math.sin(angle)
        eyeZ = game.p_pos[2] + game.g_point[2] + 20

        centerX = eyeX - math.sin(-angle) * 100
        centerY = eyeY - math.cos(-angle) * 100
        centerZ = eyeZ

        if game.cheat and not game.cheat_vision:
            eyeX = game.p_pos[0]
            eyeY = game.p_pos[1]
            eyeZ = game.p_pos[2] + 160
            centerX = eyeX + 100
            centerY = eyeY
            centerZ = eyeZ

        gluLookAt(eyeX, eyeY, eyeZ, centerX, centerY, centerZ, 0, 0, 1)
    else:
        angle = math.radians(game.cam_angle)
        x = game.cam_radius * math.sin(angle)
        y = game.cam_radius * math.cos(angle)
        z = game.cam_height
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

def spawn_enemies():
    enemies_to_spawn = 0
    base_hp = 1
    
    if game.wave == 1:
        enemies_to_spawn = 5
        base_hp = 1
        game.e_speed += 0.025
    elif game.wave == 2:
        enemies_to_spawn = 5
        base_hp = 2
        game.e_speed += 0.025
    elif game.wave == 3:
        enemies_to_spawn = 8
        base_hp = 2
        game.e_speed += 0.025
    elif game.wave == 4:
        enemies_to_spawn = 8
        base_hp = 3
        game.e_speed += 0.025
    elif game.wave == 5:
        spawn_boss()
        enemies_to_spawn = 8
        base_hp = 3
        game.e_speed += 0.025
    
    for _ in range(enemies_to_spawn):
        x = random.uniform(-grid_length + 100, grid_length - 100)
        y = random.uniform(-grid_length + 100, grid_length - 100)
        while abs(x - game.p_pos[0]) < 200:
            x = random.uniform(-grid_length + 100, grid_length - 100)
        while abs(y - game.p_pos[1]) < 200:
            y = random.uniform(-grid_length + 100, grid_length - 100)
        game.e_list.append([x, y, 0, base_hp,False])

def spawn_boss():
    x = random.choice([-1, 1]) * (grid_length - 150)
    y = random.choice([-1, 1]) * (grid_length - 150)
    game.e_list.append([x, y, 0, 10,True])  # Boss has 10 HP
    game.boss_spawned = True
    print(f"BOSS SPAWNED at ({x}, {y}) with 10 HP")

def spawn_collectibles():
    current_time = time.time()
    if current_time - game.last_spawn_time > game.spawn_interval:
        # Spawn coins (3-5 at a time)
        for _ in range(random.randint(3, 5)):
            x = random.uniform(-grid_length + 50, grid_length - 50)
            y = random.uniform(-grid_length + 50, grid_length - 50)
            game.coins.append([x, y, 30, 10])
        
        # Spawn ammo (1-2 at a time)
        for _ in range(random.randint(1, 2)):
            x = random.uniform(-grid_length + 50, grid_length - 50)
            y = random.uniform(-grid_length + 50, grid_length - 50)
            game.ammo_packs.append([x, y, 30, 10])
        
        # Spawn chest (10% chance)
        if random.random() < 0.1:
            x = random.uniform(-grid_length + 50, grid_length - 50)
            y = random.uniform(-grid_length + 50, grid_length - 50)
            game.chests.append([x, y, 40, 50])
        
        # Spawn diamond (5% chance)
        if random.random() < 0.05:
            x = random.uniform(-grid_length + 50, grid_length - 50)
            y = random.uniform(-grid_length + 50, grid_length - 50)
            game.diamonds.append([x, y, 50, 100])
        
        game.last_spawn_time = current_time

def check_collectibles():
    # Check coins
    for coin in game.coins[:]:
        dx = game.p_pos[0] - coin[0]
        dy = game.p_pos[1] - coin[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < game.player_radius + game.coin_radius:
            game.p_coins += coin[3]
            game.coins.remove(coin)
    
    # Check ammo
    for ammo in game.ammo_packs[:]:
        dx = game.p_pos[0] - ammo[0]
        dy = game.p_pos[1] - ammo[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < game.player_radius + game.ammo_radius:
            game.current_bullets = min(game.max_bullets, game.current_bullets + ammo[3])
            game.ammo_packs.remove(ammo)
    
    # Check chests
    for chest in game.chests[:]:
        dx = game.p_pos[0] - chest[0]
        dy = game.p_pos[1] - chest[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < game.player_radius + game.chest_radius:
            game.p_coins += chest[3]
            game.chests.remove(chest)
    
    # Check diamonds
    for diamond in game.diamonds[:]:
        dx = game.p_pos[0] - diamond[0]
        dy = game.p_pos[1] - diamond[1]
        distance = math.sqrt(dx*dx + dy*dy)
        if distance < game.player_radius + game.diamond_radius:
            game.p_coins += diamond[3]
            game.diamonds.remove(diamond)
    
    # Upgrade weapon
    if game.p_coins >= 300 and game.weapon_level < 3:
        game.weapon_level = 3
        game.g_bullet_speed = 2
        game.max_bullets = 50
    elif game.p_coins >= 150 and game.weapon_level < 2:
        game.weapon_level = 2
        game.g_bullet_speed = 1.5
        game.max_bullets = 40

def move_enemies():
    for enemy in game.e_list[:]:
        dx = game.p_pos[0] - enemy[0]
        dy = game.p_pos[1] - enemy[1]
        distance = math.sqrt(dx**2 + dy**2)

        if distance < game.player_radius + game.e_size:
            game.p_life -= 1
            if game.p_life <= 0:
                game.over = True
                game.e_list.clear()
                game.g_bullets.clear()
                break
            game.e_list.remove(enemy)
            spawn_enemies()
        else:
            angle = math.atan2(dy, dx)
            enemy[0] += game.e_speed * math.cos(angle)
            enemy[1] += game.e_speed * math.sin(angle)

def pulse_enemy():
    game.e_pulse_time += 0.01
    game.e_pulse = 1.0 + 0.1 * math.sin(game.e_pulse_time * 3)

def fire_bullet():
    if game.current_bullets <= 0:
        print("Out of ammo!")
        return
    
    game.current_bullets -= 1
    
    if game.first_person:
        angle = math.radians(game.p_angle + 90 / 2)
        x = game.p_pos[0] + game.g_point[0] * math.sin(angle) - game.g_point[1] * math.cos(angle)
        y = game.p_pos[1] - game.g_point[0] * math.cos(angle) - game.g_point[1] * math.sin(angle)
        z = game.p_pos[2] + game.g_point[2]
        bullet = [x, y, z, game.p_angle]
    else:
        angle = math.radians(game.p_angle - 90)
        offsetX = game.g_point[0] * math.cos(angle) - game.g_point[1] * math.sin(angle)
        offsetY = game.g_point[0] * math.sin(angle) + game.g_point[1] * math.cos(angle)
        x = game.p_pos[0] + offsetX
        y = game.p_pos[1] + offsetY
        z = game.p_pos[2] + game.g_point[2]
        bullet = [x, y, z, game.p_angle]

    game.g_bullets.append(bullet)

def move_bullets():
    to_remove = []
    for bullet in game.g_bullets[:]:
        angle = math.radians(bullet[3] - 90)
        bullet[0] += game.g_bullet_speed * math.cos(angle)
        bullet[1] += game.g_bullet_speed * math.sin(angle)

        if (bullet[0] > grid_length + 100 or bullet[0] < -grid_length or
            bullet[1] > grid_length + 100 or bullet[1] < -grid_length):
            to_remove.append(bullet)

    for bullet in to_remove:
        game.g_bullets.remove(bullet)

def hit_enemy(bullets, enemies):
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            dx = bullet[0] - enemy[0]
            dy = bullet[1] - enemy[1]
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance < game.g_bullet_size + game.e_size:
                enemy[3] -= 1  # Reduce HP
                bullets.remove(bullet)
                
                if enemy[3] <= 0:
                    # Check if it was the boss (HP > 5)
                    if enemy[4] == True and enemy[3] <= 0:
                        game.boss_defeated = True
                        print("BOSS DEFEATED!")
                    
                    game.p_score += 15 if enemy[3] > 5 else 5
                    enemies.remove(enemy)
                    
                    # Victory check
                    if (game.boss_spawned and 
                        game.boss_defeated and 
                        len(game.e_list) == 0 and 
                        game.wave >= game.max_waves):
                        game.victory_achieved = True
                        game.over = True
                        game.game_end_time = time.time()
                        print("VICTORY CONDITIONS MET!")
                    # Wave progression
                    elif len(game.e_list) == 0:
                        if game.wave < game.max_waves:
                            game.wave += 1
                            spawn_enemies()
                        elif not game.boss_spawned:
                            spawn_boss()
                break

def get_enemy_angles():
    angles = []
    for enemy in game.e_list:
        dx = game.p_pos[0] - enemy[0]
        dy = game.p_pos[1] - enemy[1]
        angles.append((math.degrees(math.atan2(dy, dx)) - 90) % 360)
    return angles

def cheat_mode_aim_rotate():
    if not game.e_list or not game.cheat:
        return

    enemy_angles = get_enemy_angles()
    game.p_angle = (game.p_angle + game.p_turn_speed / 50) % 360

    for angle in enemy_angles:
        angle_diff = abs((game.p_angle - angle + 540) % 360 - 180)
        threshold = game.cheat_angle_margin_1st if game.first_person else game.cheat_angle_margin
        if angle_diff <= threshold:
            fire_bullet()
            break

def keyboard_listener(key, a, b):
    x, y, z = game.p_pos

    if not game.over and not game.game_won:
        if key == b'w':
            x -= game.p_speed * math.sin(math.radians(-game.p_angle))
            y -= game.p_speed * math.cos(math.radians(game.p_angle))
        if key == b's':
            x += game.p_speed * math.sin(math.radians(-game.p_angle))
            y += game.p_speed * math.cos(math.radians(game.p_angle))
        if key == b'a':
            game.p_angle += game.p_turn_speed
        if key == b'd':
            game.p_angle -= game.p_turn_speed
        if key == b'c':
            game.cheat = not game.cheat
            game.e_size = 40 if game.cheat else 30
        if key == b'v':
            if game.first_person and game.cheat:
                game.cheat_vision = not game.cheat_vision

    if key == b'r':
        reset_game()

    # Boundary checks
    game.p_pos = [
        max(-grid_length, min(grid_length + 100, x)),
        max(-grid_length, min(grid_length + 100, y)),
        z
    ]

def specialKeyListener(key, a, b):
    if key == GLUT_KEY_UP:
        game.cam_height -= 10
        game.cam_radius -= 10
    if key == GLUT_KEY_DOWN:
        game.cam_height += 10
        game.cam_radius += 10
    if key == GLUT_KEY_LEFT:
        game.cam_angle -= 5
    if key == GLUT_KEY_RIGHT:
        game.cam_angle += 5

def mouse_listener(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game.over and not game.game_won:
        fire_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN and not game.over and not game.game_won:
        game.first_person = not game.first_person
        game.cheat_vision = False
        game.p_turn_speed = 2.5 if game.first_person else 5


def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, W_width, W_height)

    set_camera()
    draw_grid()
    draw_player()
    draw_collectibles()

    if not game.over:
        if game.cheat:
            cheat_mode_aim_rotate()

        for enemy in game.e_list:
            draw_enemy(*enemy)

        for bullet in game.g_bullets:
            draw_bullet(bullet[0], bullet[1], bullet[2])

        # HUD
        draw_text(10, 770, f"Life: {game.p_life}")
        draw_text(10, 740, f"Score: {game.p_score}")
        draw_text(10, 710, f"Wave: {game.wave}/{game.max_waves}")
        draw_text(10, 680, f"Coins: {game.p_coins}")
        draw_text(10, 650, f"Ammo: {game.current_bullets}/{game.max_bullets}")
        draw_text(10, 620, f"Weapon: Lvl {game.weapon_level}")
    elif game.victory_achieved:
        play_time = game.game_end_time - game.game_start_time
        minutes = int(play_time // 60)
        seconds = int(play_time % 60)
        
        # Big green victory message
        glColor3f(0, 1, 0)
        draw_text(W_width/2- 70, W_height/2 + 150, "MISSION COMPLETE!")
        
        # Stats in white
        glColor3f(1, 1, 1)
        draw_text(W_width/2- 70, W_height/2 + 80, f"Final Score: {game.p_score}")
        draw_text(W_width/2- 70, W_height/2 + 40, f"Time: {minutes}m {seconds}s")
        draw_text(W_width/2- 70, W_height/2, "All enemies eliminated!")
        draw_text(W_width/2- 70, W_height/2 - 40, "Boss destroyed!")
        
        # Restart instructions
        glColor3f(1, 1, 0)  # Yellow
        draw_text(W_width/2 - 70, W_height/2 - 100, 'Press "R" to restart')
    else:
        draw_text(W_width/2 - 100, W_height/2, f"GAME OVER - Score: {game.p_score}")
        draw_text(W_width/2 - 120, W_height/2 - 30, 'Press "R" to restart')
    
    glutSwapBuffers()



def idle():
    if not game.over and not game.game_won:
        move_enemies()
        pulse_enemy()
        move_bullets()
        hit_enemy(game.g_bullets, game.e_list)
        spawn_collectibles()
        check_collectibles()
    glutPostRedisplay()

def reset_game():
    global game
    game = GameState()
    spawn_enemies()
    print("Game reset - Ready to play!")

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(W_width, W_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Enhanced Bullet Frenzy 3D")
    glEnable(GL_DEPTH_TEST)

    reset_game()

    glutDisplayFunc(show_screen)
    glutIdleFunc(idle)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouse_listener)

    glutMainLoop()

if __name__ == "__main__":
    main()