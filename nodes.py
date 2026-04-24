import torch


class VHSForceFPSKeepSpeed:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "source_fps": ("FLOAT", {"default": 24.0, "min": 0.001, "max": 1000.0, "step": 0.001}),
                "force_fps": ("FLOAT", {"default": 12.0, "min": 0.001, "max": 1000.0, "step": 0.001}),
            }
        }

    RETURN_TYPES = ("IMAGE", "INT", "FLOAT", "INT")
    RETURN_NAMES = ("images", "frame_count", "output_fps", "dropped_frames")
    FUNCTION = "force"
    CATEGORY = "video/custom"

    @staticmethod
    def _select_indices_vhs(total_frames: int, source_fps: float, force_fps: float):
        if total_frames <= 0:
            return []

        # VHS cv loader behavior: preserve duration by selecting frames based on
        # source and target frame-time accumulation (no speed change).
        base_frame_time = 1.0 / source_fps
        target_frame_time = 1.0 / force_fps

        selected = []
        time_offset = target_frame_time
        grabbed_index = 0

        while grabbed_index < total_frames:
            if time_offset < target_frame_time:
                grabbed_index += 1
                if grabbed_index >= total_frames:
                    break
                time_offset += base_frame_time
                continue

            time_offset -= target_frame_time
            selected.append(grabbed_index)

        return selected

    def force(self, images, source_fps, force_fps):
        frame_count = int(images.shape[0])
        if frame_count == 0:
            return (images, 0, float(force_fps), 0)

        # This node is designed for "forcing down" FPS.
        if force_fps >= source_fps:
            return (images, frame_count, float(source_fps), 0)

        keep_indices = self._select_indices_vhs(frame_count, float(source_fps), float(force_fps))
        if not keep_indices:
            keep_indices = [0]

        index_tensor = torch.tensor(keep_indices, device=images.device, dtype=torch.long)
        out_images = images.index_select(0, index_tensor)
        dropped = frame_count - int(out_images.shape[0])

        return (out_images, int(out_images.shape[0]), float(force_fps), dropped)


NODE_CLASS_MAPPINGS = {
    "VHSForceFPSKeepSpeed": VHSForceFPSKeepSpeed,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VHSForceFPSKeepSpeed": "Force FPS (Keep Speed, VHS-style)",
}
