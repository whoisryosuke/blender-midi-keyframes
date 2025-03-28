---
tags:
  - export
  - godot
---

# Exporting to Godot

1. Open an existing project
2. Drag and drop the GLTF file inside the FileSystem panel (preferably in a folder you want it)
3. Accept the defaults
4. Drag and drop the GLTF node into your scene (looks like a movie clip icon).

![image.png](attachment:b7589dd1-5bc9-458f-b9b1-3624cbf23c24:image.png)

To play the animation, create a script on a node somewhere (I just picked the top-most node).

You can play the animation whenever, but I’ll be playing it here when the level loads immediately using the `on_ready()` Node method.

```python
extends Node3D

# Runs when the level loads
func _on_ready() -> void:
	# Sanity check
	#print("running")

	# Grab the GLTF model. I made it a "Unique Name"
	var animation_player = %Ryoturia.get_node("AnimationPlayer") as AnimationPlayer

	# Play the animation, usually labeled "Scene"
	# You can open the GLTF node and check the name inside the AnimationPlayer
	animation_player.play("Scene")

	pass
```
