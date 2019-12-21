from time import sleep
from onvif import ONVIFCamera
import zeep
import sys


def zeep_pythonvalue(self, xmlvalue):
    return xmlvalue


class Move:
    def __init__(self, ip, port, user, passwd):
        try:
            self.XMAX = 1
            self.XMIN = -1
            self.YMAX = 1
            self.YMIN = -1
            self.ZMAX = 1
            self.ZMIN = -1
            mycam = ONVIFCamera(ip, port, user, passwd)
            # Create media service object
            media = mycam.create_media_service()
            # Create ptz service object
            self.ptz = mycam.create_ptz_service()

            # Get target profile
            zeep.xsd.simple.AnySimpleType.pythonvalue = zeep_pythonvalue
            media_profile = media.GetProfiles()[0]

            # Get PTZ configuration options for getting continuous move range
            self.request = self.ptz.create_type('GetConfigurationOptions')
            self.request.ConfigurationToken = media_profile.PTZConfiguration.token
            ptz_configuration_options = self.ptz.GetConfigurationOptions(self.request)

            self.request = self.ptz.create_type('ContinuousMove')
            self.request.ProfileToken = media_profile.token
            self.ptz.Stop({'ProfileToken': media_profile.token})

            if self.request.Velocity is None:
                self.request.Velocity = self.ptz.GetStatus({'ProfileToken': media_profile.token}).Position
                self.request.Velocity.PanTilt.space = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[
                    0].URI
                self.request.Velocity.Zoom.space = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].URI

            # Get range of pan and tilt
            # NOTE: X and Y are velocity vector
            print(ptz_configuration_options.Spaces)
            self.XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
            self.XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
            self.YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
            self.YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min
            self.ZMAX = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].XRange.Max
            self.ZMIN = ptz_configuration_options.Spaces.ContinuousZoomVelocitySpace[0].XRange.Min
        except Exception as e:
            print(e)
            sys.exit()

    def perform_move(self, timeout):
        # Start continuous move
        self.ptz.ContinuousMove(self.request)
        # Wait a certain time
        sleep(timeout)
        # Stop continuous move
        self.ptz.Stop({'ProfileToken': self.request.ProfileToken})

    def up(self, timeout=0.1):
        print('move up...')
        self.request.Velocity.PanTilt.x = 0
        self.request.Velocity.PanTilt.y = self.YMAX
        self.perform_move(timeout)

    def down(self, timeout=0.1):
        print('move down...')
        self.request.Velocity.PanTilt.x = 0
        self.request.Velocity.PanTilt.y = self.YMIN
        self.perform_move(timeout)

    def right(self, timeout=0.1):
        print('move right...')
        self.request.Velocity.PanTilt.x = self.XMAX
        self.request.Velocity.PanTilt.y = 0
        self.perform_move(timeout)

    def left(self, timeout=0.1):
        print('move left...')
        self.request.Velocity.PanTilt.x = self.XMIN
        self.request.Velocity.PanTilt.y = 0
        self.perform_move(timeout)

    def zoom_in(self, timeout=0.1):
        print('zoom in...')
        self.request.Velocity.PanTilt.x = 0
        self.request.Velocity.PanTilt.y = 0
        self.request.Velocity.Zoom = self.ZMAX
        self.perform_move(timeout)

    def zoom_out(self, timeout=0.1):
        print('zoom out...')
        self.request.Velocity.PanTilt.x = 0
        self.request.Velocity.PanTilt.y = 0
        self.request.Velocity.Zoom = self.ZMIN
        self.perform_move(timeout)


if __name__ == '__main__':
    mc = Move('10.170.0.100', 80, 'orca', 'Gwbnsh@408')
    mc.up()
