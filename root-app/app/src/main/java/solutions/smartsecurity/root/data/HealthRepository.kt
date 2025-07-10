package solutions.smartsecurity.root.data

import solutions.smartsecurity.contracts.health.models.HealthRequest
import solutions.smartsecurity.contracts.health.models.HealthResponse
import solutions.smartsecurity.root.net.ApiService
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import okhttp3.OkHttpClient
import java.time.OffsetDateTime

class HealthRepository {
    private val api: ApiService

    init {
        val client = OkHttpClient.Builder()
            // TODO: Certificate pinning (SHA-256: "TODO_REPLACE_WITH_REAL_HASH")
            .build()
        val retrofit = Retrofit.Builder()
            .baseUrl("https://cloud.smartsecurity.solutions/")
            .addConverterFactory(MoshiConverterFactory.create())
            .client(client)
            .build()
        api = retrofit.create(ApiService::class.java)
    }

    suspend fun postHealthSample(deviceId: String, batteryPercent: Int, lteRssi: Int, wifiRssi: Int): Result<HealthResponse> {
        val request = HealthRequest(
            deviceId = deviceId,
            timestamp = OffsetDateTime.now().toString(),
            batteryPercent = batteryPercent,
            lteRssi = lteRssi,
            wifiRssi = wifiRssi
        )
        return try {
            val response = api.postHealth(request)
            if (response.isSuccessful) {
                Result.success(response.body()!!)
            } else {
                Result.failure(Exception("HTTP ${'$'}{response.code()}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
} 