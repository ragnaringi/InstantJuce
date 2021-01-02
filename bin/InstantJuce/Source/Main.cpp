/*
  ==============================================================================

    This file contains the basic startup code for a JUCE application.

  ==============================================================================
*/

#include <JuceHeader.h>
#include "../../../Context.h"

using namespace juce;

//==============================================================================
int main (int argc, char* argv[])
{
    ScopedJuceInitialiser_GUI gui_init;
    
    AudioDeviceManager deviceManager;
    
    String error = deviceManager.initialiseWithDefaultDevices (0, 2);
    if (error.isEmpty())
    {
        std::cout << "Device opened : " << deviceManager.getCurrentAudioDevice()->getName() << "\n";
        
        LiveContext tonesource;
        
        AudioSourcePlayer sourcePlayer;
        sourcePlayer.setSource (&tonesource);
        
        deviceManager.addAudioCallback (&sourcePlayer);
        
        while (deviceManager.getCurrentAudioDevice()->isPlaying())
        {
            Thread::sleep (100);
        }
        std::cout << "Closing device...\n";
    }
    else
        std::cout << "Could not open device : " << error << "\n";
    
    return 0;
}
