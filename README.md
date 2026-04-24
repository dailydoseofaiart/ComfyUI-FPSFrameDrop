# VHS Force FPS Keep Speed (ComfyUI custom node)

This node applies the same frame-time selection approach used by Video Helper Suite load video FPS forcing, but on an existing IMAGE frame batch.

## Inputs
- images (IMAGE): frame sequence tensor
- source_fps (FLOAT): FPS of the incoming frame sequence
- force_fps (FLOAT): target FPS to force to (intended for lower FPS)

## Outputs
- images (IMAGE): reduced frame sequence
- frame_count (INT): output frame count
- output_fps (FLOAT): FPS to use in your Video Combine node
- dropped_frames (INT): number of frames removed

## Install
1. Copy folder vhs_force_fps_keep_speed into your ComfyUI custom_nodes directory.
2. Restart ComfyUI.
3. Add node: Force FPS (Keep Speed, VHS-style).

## Typical wiring
... -> (IMAGE frames) -> Force FPS (Keep Speed, VHS-style) -> Video Combine

Set Video Combine FPS to the node output_fps (or the same value as force_fps).
