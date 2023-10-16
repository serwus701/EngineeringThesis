#include <windows.h>

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

void MoveWindowToRightScreen() {
    HWND hWnd = GetForegroundWindow(); // Get the current active window
    EnumDisplayMonitors(NULL, NULL, MonitorEnumProc, (LPARAM)hWnd);
}

int main() {
    MoveWindowToRightScreen();
    return 0;
}
