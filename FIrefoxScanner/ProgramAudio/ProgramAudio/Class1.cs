using System;
using System.Diagnostics;
using NAudio.CoreAudioApi;
using NAudio.CoreAudioApi.Interfaces;


namespace ProgramAudio;

public class AudioChecker
{
    public static bool IsFirefoxPlaying()
    {
        var enumerator = new MMDeviceEnumerator();
        var device = enumerator.GetDefaultAudioEndpoint(DataFlow.Render, Role.Multimedia);

        var sessions = device.AudioSessionManager.Sessions;

        for (int i = 0; i < sessions.Count; i++)
        {
            var session = sessions[i];

            try
            {
                var processId = session.GetProcessID;
                var process = Process.GetProcessById((int)processId);

                if (process.ProcessName.ToLower().Contains("firefox"))
                {
                    if (session.State == AudioSessionState.AudioSessionStateActive)
                    {
                        var audioMeter = session.AudioMeterInformation;
                        float peakValue = audioMeter.MasterPeakValue;

                        if (peakValue > 0.01)
                        {
                            Console.WriteLine("Firefox is playing: " + peakValue);
                            return true;
                        }
                        
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        Console.WriteLine("Firefox is not playing");
        return false;
    }
}