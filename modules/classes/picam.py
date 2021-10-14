from modules.classes.color import Color as color

class PiCam:

    # constants to limit kernel_blur (must be impair)
    KERNEL_BLUR_MIN = 1
    KERNEL_BLUR_MAX = 59
    KERNEL_BLUR_DEFAULT = 5

    # constants to limit surface_step
    SURFACE_STEP_MIN = 100
    SURFACE_STEP_MAX = 1000
    SURFACE_STEP_DEFAULT = 500

    # constants to limit surface_threshold
    SURFACE_THRESHOLD_MIN = 1000
    SURFACE_THRESHOLD_MAX = 10000
    SURFACE_THRESHOLD_DEFAULT = 5000

    # constants to limit mask_threshold
    MASK_THRESHOLD_MIN = 1
    MASK_THRESHOLD_MAX = 255
    MASK_THRESHOLD_DEFAULT = 15

    # constants to limit duration
    DURATION_MIN = 30
    DURATION_MAX = 60

    # constructor

    def __init__(self):
        self._kernel_blur = PiCam.KERNEL_BLUR_DEFAULT
        self._surface_step = PiCam.SURFACE_STEP_DEFAULT
        self._surface_threshold = PiCam.SURFACE_THRESHOLD_DEFAULT
        self._mask_threshold = PiCam.MASK_THRESHOLD_DEFAULT
        self._duration = PiCam.DURATION_MIN
        self._intruder = False
    
    # getters

    @property
    def kernel_blur(self):
        return self._kernel_blur

    @property
    def surface_step(self):
        return self._surface_step
    
    @property
    def surface_threshold(self):
        return self._surface_threshold

    @property
    def mask_threshold(self):
        return self._mask_threshold

    @property
    def duration(self):
        return self._duration

    @property
    def intruder(self):
        return self._intruder

    # setters

    @kernel_blur.setter
    def kernel_blur(self, new_kernel_blur):
        if isinstance(new_kernel_blur, int) and (new_kernel_blur >= PiCam.KERNEL_BLUR_MIN 
                                                and new_kernel_blur <= PiCam.KERNEL_BLUR_MAX):
            self._kernel_blur = new_kernel_blur
        else :
            print(color.RED + 'ERROR kernel_blur : the value must be between ' + 
                  str(PiCam.KERNEL_BLUR_MIN) + ' and ' +
                  str(PiCam.KERNEL_BLUR_MAX) + color.END)

    @surface_step.setter
    def surface_step(self, new_surface_step):
        if isinstance(new_surface_step, int) and (new_surface_step >= PiCam.SURFACE_STEP_MIN 
                                                 and new_surface_step <= PiCam.SURFACE_STEP_MAX):
            self._surface_step = new_surface_step
        else :
            print(color.RED + 'ERROR surface_step : the value must be between ' + 
                  str(PiCam.SURFACE_STEP_MIN) + ' and ' +
                  str(PiCam.SURFACE_STEP_MAX) + color.END)

    @surface_threshold.setter
    def surface_threshold(self, new_surface_threshold):
        if isinstance(new_surface_threshold, int) and (new_surface_threshold >= PiCam.SURFACE_THRESHOLD_MIN 
                                                      and new_surface_threshold <= PiCam.SURFACE_THRESHOLD_MAX):
            self._surface_threshold = new_surface_threshold
        else :
            print(color.RED + 'ERROR surface_threshold : the value must be between ' + 
                  str(PiCam.SURFACE_THRESHOLD_MIN) + ' and ' +
                  str(PiCam.SURFACE_THRESHOLD_MAX) + color.END)

    @mask_threshold.setter
    def mask_threshold(self, new_mask_threshold):
        if isinstance(new_mask_threshold, int) and (new_mask_threshold >= PiCam.MASK_THRESHOLD_MIN 
                                                   and new_mask_threshold <= PiCam.MASK_THRESHOLD_MAX):
            self._mask_threshold = new_mask_threshold
        else :
            print(color.RED + 'ERROR mask_threshold : the value must be between ' + 
                  str(PiCam.MASK_THRESHOLD_MIN) + ' and ' +
                  str(PiCam.MASK_THRESHOLD_MAX) + color.END)
    
    @duration.setter
    def duration(self, new_duration):
        if isinstance(new_duration, int) and (new_duration >= PiCam.DURATION_MIN 
                                             and new_duration <= PiCam.DURATION_MAX):
            self._duration = new_duration
        else :
            print(color.RED + 'ERROR duration : the value must be between ' + 
                  str(PiCam.DURATION_MIN) + ' and ' +
                  str(PiCam.DURATION_MAX) + color.END)
            print(color.RED + 'ATTENTION duration : the min value is setting...' + color.END)
            self._duration = PiCam.DURATION_MIN
    
    @intruder.setter
    def intruder(self, new_intruder):
        if isinstance(new_intruder, bool):
            self._intruder = new_intruder
        else :
            print(color.RED + 'ERROR intruder : the value must be boolean ' + color.END)
            print(color.RED + 'ATTENTION intruder : the default value is setting...' + color.END)
            self._intruder = False
            
    # increase functions

    def increase_kernel_blur(self):
            self._kernel_blur = min(PiCam.KERNEL_BLUR_MAX, (self._kernel_blur + 2))

    def increase_surface_step(self):
            self._surface_step = min(PiCam.SURFACE_STEP_MAX, (self._surface_step + 100))

    def increase_surface_threshold(self):
            self._surface_threshold = min(PiCam.SURFACE_THRESHOLD_MAX, (self._surface_threshold + self._surface_step))

    def increase_mask_threshold(self):
            self._mask_threshold = min(PiCam.MASK_THRESHOLD_MAX, (self._mask_threshold + 1))

    # decrease functions
    
    def decrease_kernel_blur(self):
            self._kernel_blur = max(PiCam.KERNEL_BLUR_MIN, (self._kernel_blur - 2))

    def decrease_surface_step(self):
            self._surface_step = max(PiCam.SURFACE_STEP_MIN, (self._surface_step - 100))

    def decrease_surface_threshold(self):
            self._surface_threshold = max(PiCam.SURFACE_THRESHOLD_MIN, (self._surface_threshold - self._surface_step))

    def decrease_mask_threshold(self):
            self._mask_threshold = max(PiCam.MASK_THRESHOLD_MIN, (self._mask_threshold - 1))
            