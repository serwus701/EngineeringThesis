Add-Type @"
    using System;
    using System.Runtime.InteropServices;
    using System.Windows.Forms;

    public class MonitorHelper {
        [DllImport("user32.dll")]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool EnumDisplayMonitors(IntPtr hdc, IntPtr lprcClip, MonitorEnumProc lpfnEnum, IntPtr dwData);

        [DllImport("user32.dll")]
        public static extern bool GetMonitorInfo(IntPtr hMonitor, ref MONITORINFOEX lpmi);

        [DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr GetForegroundWindow();

        [DllImport("user32.dll", SetLastError = true)]
        public static extern IntPtr MonitorFromWindow(IntPtr hwnd, uint dwFlags);

        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetWindowPos(IntPtr hWnd, IntPtr hWndInsertAfter, int X, int Y, int cx, int cy, uint uFlags);

        public delegate bool MonitorEnumProc(IntPtr hMonitor, IntPtr hdcMonitor, ref RECT lprcMonitor, IntPtr dwData);

        [StructLayout(LayoutKind.Sequential)]
        public struct MONITORINFOEX {
            public int cbSize;
            public RECT rcMonitor;
            public RECT rcWork;
            public int dwFlags;
            [MarshalAs(UnmanagedType.ByValTStr, SizeConst = 32)]
            public string szDevice;
        }

        [StructLayout(LayoutKind.Sequential)]
        public struct RECT {
            public int left;
            public int top;
            public int right;
            public int bottom;
        }

        public const uint MONITOR_DEFAULTTONEAREST = 2;
    }
"@

function Move-Window([bool]$isLeft) {
    $foregroundWindow = [MonitorHelper]::GetForegroundWindow()
    $hMonitor = [MonitorHelper]::MonitorFromWindow($foregroundWindow, [MonitorHelper]::MONITOR_DEFAULTTONEAREST)

    $monitorInfo = New-Object MonitorHelper+MONITORINFOEX
    $monitorInfo.cbSize = [System.Runtime.InteropServices.Marshal]::SizeOf($monitorInfo)
    [MonitorHelper]::GetMonitorInfo($hMonitor, [ref]$monitorInfo)

    $sourceMonitor = 0  # 0 for left, 1 for middle, 2 for right
    if ($monitorInfo.rcMonitor.left -lt 0) {
        $sourceMonitor = 0  # Window is on the left monitor
    } elseif ($monitorInfo.rcMonitor.left -lt 1920) {
        $sourceMonitor = 1  # Window is on the middle monitor
    } else {
        $sourceMonitor = 2  # Window is on the right monitor
    }

    $destinationMonitor = if ($isLeft) { ($sourceMonitor - 1) % 3 } else { ($sourceMonitor + 1) % 3 }

    if ($destinationMonitor -eq 0) {
        # Move to the left monitor
        [MonitorHelper]::SetWindowPos($foregroundWindow, [IntPtr]::Zero, -1920, 0, 0, 0, 0x1 | 0x4)
    } elseif ($destinationMonitor -eq 1) {
        # Move to the middle monitor
        [MonitorHelper]::SetWindowPos($foregroundWindow, [IntPtr]::Zero, 0, 0, 0, 0, 0x1 | 0x4)
    } else {
        # Move to the right monitor
        [MonitorHelper]::SetWindowPos($foregroundWindow, [IntPtr]::Zero, 1920, 0, 0, 0, 0x1 | 0x4)
    }
}

# Usage
Move-Window -isLeft $true
