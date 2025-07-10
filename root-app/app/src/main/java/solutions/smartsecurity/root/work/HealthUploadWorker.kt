package solutions.smartsecurity.root.work

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import solutions.smartsecurity.root.data.HealthRepository
import android.os.BatteryManager
import android.content.Context.BATTERY_SERVICE
import android.telephony.TelephonyManager
import android.net.wifi.WifiManager
import android.net.wifi.WifiInfo
import android.util.Log

class HealthUploadWorker(
    appContext: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(appContext, workerParams) {
    override suspend fun doWork(): Result {
        val repo = HealthRepository()
        val deviceId = android.os.Build.SERIAL ?: "unknown"
        val batteryPercent = getBatteryPercent(applicationContext)
        val lteRssi = getLteRssi(applicationContext)
        val wifiRssi = getWifiRssi(applicationContext)
        Log.d("HealthUploadWorker", "Sampled: battery=$batteryPercent, lte=$lteRssi, wifi=$wifiRssi")
        val result = repo.postHealthSample(deviceId, batteryPercent, lteRssi, wifiRssi)
        return if (result.isSuccess) Result.success() else Result.retry()
    }

    private fun getBatteryPercent(context: Context): Int {
        val bm = context.getSystemService(BATTERY_SERVICE) as BatteryManager
        return bm.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY)
    }

    private fun getLteRssi(context: Context): Int {
        val tm = context.getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager
        // TODO: Use proper API for LTE/5G RSSI (requires permissions)
        return -1 // Placeholder
    }

    private fun getWifiRssi(context: Context): Int {
        val wm = context.applicationContext.getSystemService(Context.WIFI_SERVICE) as WifiManager
        val info: WifiInfo? = wm.connectionInfo
        return info?.rssi ?: -1
    }
} 