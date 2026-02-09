#!/usr/bin/env python3
"""
One-time script to extract FAQ translations from the app's Localizable.xcstrings.

Usage: python3 extract_faq.py > faq_translations.json

Reads the xcstrings file, finds all 38 FAQ question/answer strings,
and outputs them grouped by language in the format needed by our locale JSON files.
"""

import json
import os
import sys

XCSTRINGS_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    '..', '..', '..', 'IceTimeTrack',
    'Ice Time Track', 'Ice Time Track Phone', 'Localizable.xcstrings'
)

# The 34 FAQ items in order (matching FAQData.swift categories)
FAQ_QUESTIONS = [
    # Getting Started
    "How do I start tracking a session?",
    "What's the difference between Game, Practice, and Scrimmage?",
    "Do I need my iPhone with me during a game?",
    # Movement Detection
    "What is a step?",
    "What is acceleration?",
    "What is rotation?",
    # Shift Detection
    "How does the app know when I'm on the ice?",
    "How is on-ice/bench status triggered by motion?",
    "How do the advanced detection settings work?",
    "Why is there a delay when I stop skating?",
    "What is the movement buffer?",
    # Live Game Log
    "What is the game log?",
    "Do I need to start a Game session to use the game log?",
    "Can I log a game result without starting a live tracking session on the Apple Watch?",
    "How do I log events on my Watch?",
    "How do I log events on my iPhone?",
    "What types of events can I log?",
    "What happens if I don't set a time for an event?",
    "Can I edit events after the session?",
    "How are Watch and iPhone events merged?",
    # Settings & Customization
    "What does detection sensitivity do?",
    "How do I adjust the buffer time?",
    "What are haptic alerts and how do I use them?",
    'What does "Auto-end session" do?',
    "If I change settings during an active session, do they take effect immediately?",
    "What are Advanced Settings?",
    # Health & Fitness Data
    "What data is saved to Apple Health?",
    "How do I enable/disable HealthKit integration?",
    "Why isn't my heart rate showing?",
    # Syncing & Data
    "How do sessions sync between Watch and iPhone?",
    "Why isn't my session showing on my iPhone?",
    "Can I delete a session?",
    # Troubleshooting
    "The app isn't detecting my shifts accurately",
    "The app stopped recording mid-game",
    "The Watch app is stuck on 'Sync Required'",
    # Privacy & Permissions
    "Why does the app need location access?",
    "Why does the app need motion & fitness access?",
    "Is my data shared with anyone?",
    "How do I enable location access if I accidentally denied it?",
]

# The corresponding answer keys (same English text as in FAQData.swift)
FAQ_ANSWERS = [
    # Getting Started
    "Open the Ice Time Track app on your Apple Watch. Select your session type (Game, Practice, Scrimmage, or Other) and tap to begin. The app will automatically start detecting when you're on the ice versus on the bench.",
    "These are labels to help you organize your sessions. Game is for official matches, Practice for team practices, Scrimmage for informal games, and Other for anything else like public skating. The detection works the same for all types.",
    "No. The Apple Watch records everything independently. Your session will sync to your iPhone automatically when the devices are in range after the game.",
    # Movement Detection
    'A "step" is detected by your Apple Watch when it senses a rhythmic arm swing pattern using its accelerometer. It doesn\'t actually detect your foot hitting the ground - instead, it recognizes the arm motion that accompanies movement. During hockey, your skating stride and stick handling create similar arm movements, so the app uses "steps per second" as one indicator of active play.',
    "Acceleration measures how quickly you're speeding up, slowing down, or changing direction. Your Apple Watch's accelerometer detects this motion in three dimensions. Hard stops, explosive starts, and quick direction changes during a breakout all register as high acceleration - while sitting on the bench waiting for your next shift shows minimal activity.",
    "Rotation measures how much and how fast you're turning or spinning. Your Apple Watch's gyroscope detects this movement, which is especially common in hockey - crossovers through the neutral zone, pivoting to skate backwards on defense, or spinning off a check all create distinct rotation patterns. Combined with acceleration, this helps the app distinguish active skating from standing still.",
    # Shift Detection
    "The app combines multiple sensors: the accelerometer detects movement intensity, the pedometer tracks your skating stride, and GPS measures your speed. When you're actively skating, these sensors show high activity. When you're sitting on the bench, activity drops significantly.",
    'Your Watch reads movement intensity, skating stride, and GPS speed. When the app detects strong enough motion from these sensors, it marks you as on-ice. When all three drop to low levels and stay there, it starts the transition to bench.\n\nThe Sensitivity setting controls how much movement is needed:\n\n\u2022 High \u2014 Picks up lighter movements. Use this if your shifts aren\'t being detected.\n\u2022 Medium \u2014 Balanced for most players. This is the default.\n\u2022 Low \u2014 Needs stronger movement to count as skating. Use this if you\'re getting false on-ice readings while on the bench.',
    'Advanced Settings give you full control over every detection threshold. Adjusting any slider automatically switches your sensitivity to "Custom."\n\nOn-Ice Trigger \u2014 To be marked as skating, EITHER your GPS speed must exceed its threshold for 3 seconds, OR both your acceleration and step cadence must exceed theirs for the hold duration.\n\u2022 Acceleration: 0.2\u20133.0G (default: 0.2G)\n\u2022 Step Cadence: 0.4\u20132.0 steps/sec (default: 0.8)\n\u2022 GPS Speed: 0.5\u20133.0 m/s (default: 1.5)\n\u2022 Hold Duration: 1\u20135 sec (default: 2s)\n\nOn-Bench Trigger \u2014 To transition to bench, ALL three readings must drop below their thresholds for the hold duration.\n\u2022 Acceleration: 0.3\u20131.5G (default: 0.7G)\n\u2022 Step Cadence: 0.4\u20131.5 steps/sec (default: 1.0)\n\u2022 GPS Speed: 0.1\u20131.0 m/s (default: 0.5)\n\u2022 Hold Duration: 1\u20135 sec (default: 3s)\n\nWe recommend using the preset levels (High, Medium, Low) unless you need fine-grained tuning. Tap "Reset to Preset" anytime to revert.',
    'This is the "movement buffer" - a short waiting period (default 20 seconds) before the app confirms you\'re back on the bench. This prevents brief pauses during a shift from being counted as bench time.',
    'The movement buffer is a configurable delay (10-30 seconds) that prevents false shift endings. When you stop moving, the app waits this amount of time before marking you as "on bench." If you start moving again during the buffer, your shift continues uninterrupted.',
    # Live Game Log
    "The game log lets you record events during a session \u2014 goals for, goals against, penalties, and period starts. Events are logged from your Apple Watch during play and can also be added from your iPhone. The score and personal stats (my goals, my assists, penalty minutes) are calculated from the events you log.",
    "No. The game log is available for all session types \u2014 Game, Practice, Scrimmage, and Other. You can log goals and penalties in any session.",
    'Yes. Tap the + button next to "Recent Sessions" on the Dashboard to add a manual game record. You can enter the score, opponent, goals, assists, penalties, and period information \u2014 all without wearing your Watch. This is useful for logging games after the fact or for analytical purposes.',
    "During an active session, tap the LOG button at the bottom of the screen. Select the event type (goal for, goal against, penalty, or period start) and fill in the details. The event is recorded with the current time and appears on your iPhone within seconds.",
    "While a session is active on your Watch, open the iPhone app to see your live session. Events logged on the Watch appear on your iPhone in real time. You can also add or delete events directly from the iPhone. Note that edits made on the iPhone are not sent back to the Watch during the session \u2014 the Watch continues showing its own log. When the session ends, both sources are merged automatically, and any changes you made on the iPhone (additions and deletions) take priority.",
    'Four types: Goal For (optionally mark "I Scored" or "I Assisted"), Goal Against, Penalty (with penalty type, duration, and whether it\'s against your team or the opponent), and Period Start (marks intermissions in your timeline).',
    "If you add an event without specifying a timestamp, it is saved without one. The event still appears in your game log and counts toward your score and stats. You can always go back and add or correct the time after the session from the session detail page on your iPhone.",
    "Yes. Open the session on your iPhone and tap any event to edit its details \u2014 type, timestamp, personal involvement (scored/assisted), penalty info, and more. You can also add new events or delete existing ones. All changes are saved immediately.",
    "During the session, the Watch and iPhone each keep their own record. When the session ends and the Watch sends the final data to your iPhone, the app merges both sources: events you deleted on the iPhone are removed, events you added on the iPhone are included, and the score is recalculated from the merged list. The final result is saved as one unified session.",
    # Settings & Customization
    'Sensitivity controls how much movement is needed to register as "skating." High sensitivity detects lighter movements (good if shifts aren\'t being detected). Low sensitivity requires stronger movement (good if you\'re getting false detections while on the bench). Medium is the default and works well for most players.',
    'Open the Ice Time Track app on your iPhone, go to Settings, and adjust the "Movement Buffer" picker. Shorter buffers (10-15 seconds) end shifts faster. Longer buffers (25-30 seconds) are more forgiving of brief pauses during shifts.',
    "Haptic alerts are vibration notifications on your Watch when your status changes. You can set them to vibrate when you step on the ice, when you return to the bench, both, or turn them off entirely. This helps you stay aware without looking at your Watch.",
    "Auto-end automatically stops your session after a set time (default 100 minutes). This prevents the app from running indefinitely if you forget to end it manually, which saves battery and ensures your data is saved.",
    "Yes. Changes to sensitivity, movement buffer, and haptic alerts sync to your Watch and take effect immediately during an ongoing session. You don't need to wait for the next session - adjustments apply within seconds of changing them on your iPhone.",
    'Advanced Settings let you fine-tune each detection threshold individually. Expand the section in Detection settings to configure acceleration, step cadence, GPS speed, and hold duration for both on-ice and on-bench triggers. When you adjust any slider, sensitivity automatically switches to "Custom". Use "Reset to Preset" to go back to Low/Medium/High presets.',
    # Health & Fitness Data
    "When enabled, the app saves your session as a Hockey workout including: duration, active calories burned, and heart rate data (average and maximum). This contributes to your Activity rings and fitness history.",
    'Open Settings in the iPhone app and toggle "Save to Apple Health." When enabled, completed sessions are saved as workouts. When disabled, your data stays only within Ice Time Track.',
    "Make sure your Watch is worn snugly and the heart rate sensor has good skin contact. Heart rate may take 30-60 seconds to appear after starting a session. If issues persist, check that Ice Time Track has permission to read heart rate in Settings > Privacy > Health.",
    # Syncing & Data
    "Sessions sync automatically when both devices are in range and connected. After you end a session on your Watch, it transfers to your iPhone within a few seconds to a few minutes. You can also manually trigger a sync from the iPhone app.",
    "First, make sure the session has ended on your Watch. Open both apps and ensure Bluetooth is enabled. Sessions sync when the Watch app is open or shortly after ending. If it still doesn't appear, try opening the Watch app again to trigger the sync.",
    "Yes. In the iPhone app, go to your sessions list, swipe left on the session you want to remove, and tap Delete. This removes it from both devices.",
    # Troubleshooting
    "Try adjusting the detection sensitivity in Settings. If shifts aren't being detected, increase sensitivity to High. If you're getting false detections on the bench, decrease to Low. Also ensure your Watch is worn securely on your wrist, not over thick gloves.",
    "This can happen if the Watch restarts or the app crashes. Check if auto-end triggered earlier than expected (adjustable in Settings).",
    "The Watch and iPhone apps need to communicate to complete initial setup. Make sure the iPhone app is open while setting up the Watch. If the screen persists, force-quit both apps and relaunch them. If the issue continues, delete and reinstall both the iPhone and Watch apps.",
    # Privacy & Permissions
    "Location (GPS) is used to measure your skating speed, which helps accurately detect when you're on the ice versus the bench. GPS data stays on your devices and is not uploaded anywhere.",
    "Motion sensors (accelerometer and gyroscope) detect your movement patterns to distinguish skating from sitting. Fitness access allows reading your step count to improve detection accuracy. This data is processed entirely on your Watch.",
    "No. All your session data, health metrics, and sensor readings stay on your Apple Watch and iPhone. Nothing is uploaded to external servers. Your data is yours.",
    'Option 1 (on Watch): Open Settings > Privacy & Security > Location Services > Ice Time Track, then select "While Using". Option 2 (from iPhone): Open the Watch app > Privacy > Location Services > Ice Time Track and enable access.',
]

LANGUAGES = ['cs', 'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja', 'ko', 'nb', 'ru', 'sk', 'sv']


def main():
    # Resolve the path
    xcstrings_path = os.path.abspath(XCSTRINGS_PATH)
    if not os.path.exists(xcstrings_path):
        print(f"Error: xcstrings file not found at {xcstrings_path}", file=sys.stderr)
        sys.exit(1)

    with open(xcstrings_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    strings = data.get('strings', {})

    result = {}

    for lang in LANGUAGES:
        faq_items = []
        for q_key, a_key in zip(FAQ_QUESTIONS, FAQ_ANSWERS):
            # Get question translation
            q_entry = strings.get(q_key, {})
            q_localizations = q_entry.get('localizations', {})
            q_lang_entry = q_localizations.get(lang, {})
            q_unit = q_lang_entry.get('stringUnit', {})
            q_translated = q_unit.get('value', q_key)

            # Get answer translation
            a_entry = strings.get(a_key, {})
            a_localizations = a_entry.get('localizations', {})
            a_lang_entry = a_localizations.get(lang, {})
            a_unit = a_lang_entry.get('stringUnit', {})
            a_translated = a_unit.get('value', a_key)

            faq_items.append({
                'question': q_translated,
                'answer': a_translated
            })

        result[lang] = faq_items

    # Output as JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
