package solutions.smartsecurity.root.net

import retrofit2.http.Body
import retrofit2.http.POST
import retrofit2.Response
import solutions.smartsecurity.contracts.health.models.HealthRequest
import solutions.smartsecurity.contracts.health.models.HealthResponse

interface ApiService {
    @POST("/api/root/v1/health")
    suspend fun postHealth(@Body body: HealthRequest): Response<HealthResponse>
} 