def user_interface():
	"""user interface
	
	Parameters: None
	
	Returns: None
	"""
	# Design the user interface that instruct users
	print("Hello! This is your BMI Calculator!\nI can help you to assess your Body Mass Index.")
	print("Please follow the following instructions.\n__________________________________")
	print("Please choose in which units that you would like to enter your weights/heights")
	# Get user's weight and height
	weight, height = user_input()
	return (weight, height)


def user_input():
	"""collect the user inputs
	Parameters: None
	
	Returns: None
	"""
	# If the user thinks he/she entered a wrong number, he can re-enter again
	choice = "No"
	while choice == "No":
		print("1: kilograms/meters\n2: pounds/inches\nPlease enter your choice:")
		unit = int(input())
		print("Please enter your weight:")
		weight = float(input())
		print("Please enter your height:")
		height = float(input())
		print("The weight/height you entered is {}/{}\nIs that correct?\nPlease enter Yes or No".format(weight, height))
		choice = input()
	#if the users use pound and inch as units, turn them into kg ang meter
	if unit == 2:
		weight = weight/2.205
		height = height/39.37
	return (weight, height)
	
def bmi_calculate(weight, height):
	"""calculate the body weight index
	Parameters:
	weight (float): weight of user
	height (float): height of user
	
	Returns:
	health_cond (string): health condition of user
	"""
	# The equation to compute the body weight index
	bmi = weight/(height**2)
	health_cond = ""
	if (bmi < 18.5):
		health_cond = "underweight"
	if (18.5 <= bmi < 25):
		health_cond = "normal weight"
	if (25 <= bmi < 30):
		health_cond = "overweight"
	if (bmi >= 30):
		health_cond = "obese"
	return health_cond
	
def user_output(health_cond):
	"""output information to terminal and save files
	Parameters:
	health_cond (string): health condition of user
	
	Returns:
	None
	"""
	print("You are " + health_cond + " !")
	print("Do you want to save the record?\nPlease enter Yes/No")
	# Let the users to choose if they want to save their BMI records
	verbose = input()
	if verbose == "Yes":
		print("Please enter the file name:")
		file_name = input()
		now = datetime.now()
		date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
		if path.exists(file_name) == True:
			with open(file_name, "a") as file_object:
				file_object.write("\n" + date_time + " You are " + health_cond + " !")
		else: 
			with open(file_name, "w") as file_object:
				file_object.write(date_time + " You are " + health_cond + " !")
	return
	
if __name__ == "__main__":
	from os import path
	# Make it possible to write current time into the current file.
	from datetime import datetime
	weight, height = user_interface()
	health_cond = bmi_calculate(weight, height)
	user_output(health_cond)
	

