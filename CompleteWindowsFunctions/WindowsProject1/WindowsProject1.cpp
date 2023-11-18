#include <windows.h>
#include <iostream>

BOOL CALLBACK MonitorEnumProc(HMONITOR hMonitor, HDC hdcMonitor, LPRECT lprcMonitor, LPARAM dwData) {
    MONITORINFOEX mi;
    mi.cbSize = sizeof(mi);
    GetMonitorInfo(hMonitor, &mi);

    // Assuming you want to move it to the right monitor, you can identify it based on the monitor position.
    if (mi.dwFlags & MONITORINFOF_PRIMARY) {
        // This is the primary monitor, do nothing or handle as needed.
    } else {
        // This is a secondary monitor, move window here.
        HWND hWnd = (HWND)dwData;
        SetWindowPos(hWnd, NULL, mi.rcMonitor.left, mi.rcMonitor.top, 0, 0, SWP_NOSIZE | SWP_NOZORDER);
    }

    return TRUE;
}

void MoveWindow(bool isLeft) {
    HWND foregroundWindow = GetForegroundWindow();
    HMONITOR hMonitor = MonitorFromWindow(foregroundWindow, MONITOR_DEFAULTTONEAREST);

    MONITORINFO monitorInfo;
    monitorInfo.cbSize = sizeof(MONITORINFO);
    GetMonitorInfo(hMonitor, &monitorInfo);


    int sourceMonitor; // 0 for left, 1 for middle, 2 for right
    if (monitorInfo.rcMonitor.left < 0) {
        sourceMonitor = 0; // Window is on the left monitor
    }
    else if (monitorInfo.rcMonitor.left < 1920) {
        sourceMonitor = 1; // Window is on the middle monitor
    }
    else {
        sourceMonitor = 2; // Window is on the right monitor
    }

    int destinationMonitor;
    if (isLeft) {
        destinationMonitor = (sourceMonitor - 1) % 3;
    }
    else {
        destinationMonitor = (sourceMonitor + 1) % 3;
    }

    if (destinationMonitor == 0) {
        // Move to the left monitor
        SetWindowPos(foregroundWindow, NULL, -1920, 0, 0, 0, SWP_NOSIZE | SWP_NOZORDER);
    }
    else if (destinationMonitor == 1) {
        // Move to the middle monitor
        SetWindowPos(foregroundWindow, NULL, 0, 0, 0, 0, SWP_NOSIZE | SWP_NOZORDER);
    }
    else {
        // Move to the right monitor
        SetWindowPos(foregroundWindow, NULL, 1920, 0, 0, 0, SWP_NOSIZE | SWP_NOZORDER);
    }
}

void MutePC() {
    HWND hwndVolume = FindWindow(L"WMPlayerApp", NULL);

    // Send the mute command to the system volume control
    SendMessage(hwndVolume, WM_APPCOMMAND, 0, APPCOMMAND_VOLUME_MUTE);
}

void LockMyPC() {
    LockWorkStation();
}

void ShowDesktop(){
    keybd_event(VK_LWIN, 0, 0, 0);  // Press the left Windows key
    keybd_event('D', 0, 0, 0);      // Press the 'D' key
    keybd_event('D', 0, KEYEVENTF_KEYUP, 0);  // Release the 'D' key
    keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0);  // Release the left Windows key

}


void switchVirtualDesktopR() {
    keybd_event(VK_LCONTROL, 0, 0, 0);  // Press the left Windows key
    keybd_event(VK_LWIN, 0, 0, 0);      // Press the 'D' key
    keybd_event(VK_RIGHT, 0, 0, 0);      // Press the 'D' key

    keybd_event(VK_LCONTROL, 0, KEYEVENTF_KEYUP, 0);  // Release the 'D' key
    keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0);  // Release the left Windows key
    keybd_event(VK_RIGHT, 0, KEYEVENTF_KEYUP, 0);  // Release the left Windows key
}

void switchVirtualDesktopL() {
    keybd_event(VK_LCONTROL, 0, 0, 0);  // Press the left Windows key
    keybd_event(VK_LWIN, 0, 0, 0);      // Press the 'D' key
    keybd_event(VK_LEFT, 0, 0, 0);      // Press the 'D' key

    keybd_event(VK_LCONTROL, 0, KEYEVENTF_KEYUP, 0);  // Release the 'D' key
    keybd_event(VK_LWIN, 0, KEYEVENTF_KEYUP, 0);  // Release the left Windows key
    keybd_event(VK_LEFT, 0, KEYEVENTF_KEYUP, 0);  // Release the left Windows key
}

int CALLBACK WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {

        //MoveWindow(true);
        //LockMyPC();
        //ToggleMutePC();
        //ShowDesktop();
        //switchVirtualDesktopL();
    MutePC();



    return 0;
}