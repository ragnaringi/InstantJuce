
#include <JuceHeader.h>

using namespace juce;

class LiveContext : public AudioSource
{
public:
    //==============================================================================
    LiveContext()
    {
        toneGenerator.setFrequency (440.0);
        toneGenerator.setAmplitude (0.1);
    }

    //==============================================================================
    void prepareToPlay (int samplesPerBlockExpected, double sampleRate) override
    {
        toneGenerator.prepareToPlay (samplesPerBlockExpected, sampleRate);
    }
    
    void releaseResources() override
    {
        
    }

    void getNextAudioBlock (const AudioSourceChannelInfo& block) override
    {
        // Write your dsp here
        
        toneGenerator.getNextAudioBlock (block);
    }

private:
    //==============================================================================
    ToneGeneratorAudioSource toneGenerator;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (LiveContext)
};

