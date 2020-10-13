import pytest
from bmi_calculator import bmi_calculate

@pytest.mark.parametrize("weight, height, BMI", [
				(70, 1.75, "normal weight"),
				(53, 1.7, "underweight"),
				(100, 1.6, "obese"),
				(91, 1.8, "overweight")
													])
													
def test_bmi_calculate(weight, height, BMI):
	assert bmi_calculate(weight, height) == BMI
