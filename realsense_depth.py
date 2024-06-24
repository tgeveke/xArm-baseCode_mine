class DepthCamera:
    import pyrealsense2 as rs
    import numpy as np

    def __init__(self):
        print('DepthCamera init() function')
        # Configure depth and color streams
        self.pipeline = self.rs.pipeline()
        config = self.rs.config()
        # Get device product line for setting a supporting resolution
        pipeline_wrapper = self.rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        device_product_line = str(device.get_info(self.rs.camera_info.product_line))

        config.enable_stream(self.rs.stream.depth, 640, 480, self.rs.format.z16, 30)
        config.enable_stream(self.rs.stream.color, 640, 480, self.rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

    def get_frame(self):
        print('get_frame() function')
        try:
            frames = self.pipeline.wait_for_frames()
            print('Got frames')
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            depth_image = self.np.asanyarray(depth_frame.get_data())
            color_image = self.np.asanyarray(color_frame.get_data())
            print('Returning from get_frame() successful!')
            return True, depth_image, color_image
        except:
            print('Error in get_frame() function')
            return False, None, None

    def new_get_frame(self):


    def release(self):
        self.pipeline.stop()
