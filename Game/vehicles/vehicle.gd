extends VehicleBody3D

const STEER_SPEED = 1.5
const STEER_LIMIT = 0.4
const BRAKE_STRENGTH = 2.0

@export var engine_force_value := 40.0

var previous_speed := linear_velocity.length()
var _steer_target := 0.0

@onready var desired_engine_pitch: float = $EngineSound.pitch_scale
const mmin = 40
const mmax = 700
const mmid = 1080/2

func mx3(x_val,x1,x2,y1,y2):
	# linear interpolation
	return y1 + (x_val - x1) * (y2 - y1) / (x2 - x1)

func Mouse_accelV1():
	print(get_viewport().get_mouse_position().y)
	var diff :float = get_viewport().get_mouse_position().y
	var op :float = mx3(diff,-mmax,mmax,-1,1)
	#print(diff)
	if diff > 100:
		Input.action_press("accelerate")
	elif diff < 100 :
		Input.action_press("accelerate")

func Mouse_steeringV2():
	var diff :float = mmid - get_viewport().get_mouse_position().x
	var op :float = mx3(diff,-mmax,mmax,-1,1)
	if abs(diff) > mmin:
		#print(op)
		return op
	else:
		return 0

func _physics_process(delta: float) -> void:
	# =======================================================
	_steer_target = Mouse_steeringV2() #Input.get_axis(&"turn_right", &"turn_left")
	_steer_target *= STEER_LIMIT
	#print(_steer_target)
	# ==========
	#Mouse_accelV1()
	#_steer_target *= STEER_LIMIT
	# Engine sound simulation (not realistic, as this car script has no notion of gear or engine RPM).
	desired_engine_pitch = 0.05 + linear_velocity.length() / (engine_force_value * 0.5)
	# Change pitch smoothly to avoid abrupt change on collision.
	$EngineSound.pitch_scale = lerpf($EngineSound.pitch_scale, desired_engine_pitch, 0.2)

	if abs(linear_velocity.length() - previous_speed) > 1.0:
		# Sudden velocity change, likely due to a collision. Play an impact sound to give audible feedback,
		# and vibrate for haptic feedback.
		$ImpactSound.play()
		Input.vibrate_handheld(100)
		for joypad in Input.get_connected_joypads():
			Input.start_joy_vibration(joypad, 0.0, 0.5, 0.1)

	# Automatically accelerate when using touch controls (reversing overrides acceleration).
	if DisplayServer.is_touchscreen_available() or Input.is_action_pressed(&"accelerate"):
		# Increase engine force at low speeds to make the initial acceleration faster.
		var speed := linear_velocity.length()
		if speed < 5.0 and not is_zero_approx(speed):
			engine_force = clampf(engine_force_value * 5.0 / speed, 0.0, 100.0)
		else:
			engine_force = engine_force_value

		if not DisplayServer.is_touchscreen_available():
			# Apply analog throttle factor for more subtle acceleration if not fully holding down the trigger.
			engine_force *= Input.get_action_strength(&"accelerate")
	else:
		engine_force = 0.0

	if Input.is_action_pressed(&"reverse"):
		# Increase engine force at low speeds to make the initial reversing faster.
		var speed := linear_velocity.length()
		if speed < 5.0 and not is_zero_approx(speed):
			engine_force = -clampf(engine_force_value * BRAKE_STRENGTH * 5.0 / speed, 0.0, 100.0)
		else:
			engine_force = -engine_force_value * BRAKE_STRENGTH

		# Apply analog brake factor for more subtle braking if not fully holding down the trigger.
		engine_force *= Input.get_action_strength(&"reverse")

	steering = move_toward(steering, _steer_target, STEER_SPEED * delta)

	previous_speed = linear_velocity.length()
