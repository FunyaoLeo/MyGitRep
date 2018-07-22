#!/usr/bin/
#This code was written by Caleb G. Teague in 2017


import numpy as np
import math
import time

lines = []

transponders = [[5.0, 5.0], [15.0, 5.0], [10.0, -5.0]] #Holds the known locations of all transponders
myPos = [0,0]
#radii = [5.0, 5.0, 5.0] #Holds the radii of transponders which are in range -MUST BE FLOATS
radii = [5.0, 5.0, 10.0]

def findPos_part1():
	i = 0
	points = [] #contains 1x2 matrices of (x,y) points	
	while (i < len(radii) - 1):
		j = i + 1
		while (j < len(radii)):
			a_mag = radii[i]
			b_mag = radii[j]
			#c is the line between the two transponders
			c = [transponders[j][0] - transponders[i][0], transponders[j][1] - transponders[i][1]]
			c_mag = math.sqrt(c[0]**2 + c[1]**2)
			
			if a_mag + b_mag > c_mag: #If the lines are long enough to make a triangle
				#numpy is used here to allow me to multiply a vector by a scalar
				#a_prime = np.array(c) * ((a_mag**2 + c_mag**2 - b_mag**2) / c_mag**2)#a projected onto c
				a_prime = np.array(c) * ((a_mag**2 + c_mag**2 - b_mag**2) / (2 * c_mag**2))#a projected onto c
				#points.append(a_prime + transponders[i])
				
				#new:
				a = math.tan(math.atan2(-c[0], c[1])) #tan and atan2 are used to avoid errors from zero and infinite slope
				point = (a_prime + transponders[i]).tolist()
				b = point[1] - a*point[0] #y_value - a*x_value
				lines.append([a, b])
			else:
				a_prime = np.array(c) * (a_mag / (a_mag + b_mag))
				#points.append(a_prime + transponders[i])
				
				#new:
				a = math.tan(math.atan2(-c[0], c[1])) #tan and atan2 are used to avoid errors from zero and infinite slope
				point = (a_prime + transponders[i]).tolist()
				b = point[1] - a*point[0] #y_value - a*x_value
				lines.append([a, b])
			j += 1
		i += 1
# #This is just averaging the points found.
	# print points
	# if(len(points) > 0):
		# x_sum = 0
		# y_sum = 0
		# for point in points:
			# x_sum += point[0]
			# y_sum += point[1]
		# myPos[0] = x_sum / len(points)
		# myPos[1] = y_sum / len(points)

		


def findPos_part2():
	i = 0
	intersections = [] #contains 1x2 matrices of (x,y) intersects	
	while (i < len(lines) - 1):
		j = i + 1
		while (j < len(lines)):
			#lines[i][0] is a, and lines[i][1] is b
			if (lines[i][0] != lines[j][0]): #Making sure they aren't parralel
				A = np.matrix([[lines[i][0], -1], [lines[j][0], -1]])
				B = np.matrix([[-1*lines[i][1]], [-1*lines[j][1]]])
				X = A.getI()*B
				intersections.append(X.transpose().tolist()[0]) #X.transpose().tolist()[0] just returns the x,y values in a list [x,y].
			j += 1
		i += 1
#This is just averaging the intersections found, another method may be better but this works for now.
	if(len(intersections) > 0):
		x_sum = 0
		y_sum = 0
		for point in intersections:
			x_sum += point[0]
			y_sum += point[1]
		myPos[0] = x_sum / len(intersections)
		myPos[1] = y_sum / len(intersections)
		
def main():
	"""
	t0 = time.time()
	for x in range(10000): findPos()
	t1 = time.time()
	print t1 - t0
	"""
	findPos_part1()
	findPos_part2()
	print myPos
	
if __name__ == "__main__":
	main()
