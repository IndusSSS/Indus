package solutions.smartsecurity.root

import androidx.test.ext.junit.runners.AndroidJUnit4
import com.squareup.moshi.Moshi
import okhttp3.mockwebserver.MockResponse
import okhttp3.mockwebserver.MockWebServer
import org.junit.After
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import retrofit2.Retrofit
import retrofit2.converter.moshi.MoshiConverterFactory
import solutions.smartsecurity.contracts.health.models.HealthRequest
import solutions.smartsecurity.contracts.health.models.HealthResponse
import solutions.smartsecurity.root.net.ApiService
import kotlinx.coroutines.runBlocking
import kotlin.test.assertEquals

@RunWith(AndroidJUnit4::class)
class HealthIntegrationTest {
    private lateinit var server: MockWebServer
    private lateinit var api: ApiService

    @Before
    fun setUp() {
        server = MockWebServer()
        server.start()
        val retrofit = Retrofit.Builder()
            .baseUrl(server.url("/"))
            .addConverterFactory(MoshiConverterFactory.create(Moshi.Builder().build()))
            .build()
        api = retrofit.create(ApiService::class.java)
    }

    @After
    fun tearDown() {
        server.shutdown()
    }

    @Test
    fun testPostHealth() = runBlocking {
        val responseJson = """{"status":"ok"}"""
        server.enqueue(MockResponse().setBody(responseJson).setResponseCode(200))
        val req = HealthRequest(
            deviceId = "test-device",
            timestamp = "2025-07-10T12:00:00Z",
            batteryPercent = 88,
            lteRssi = -70,
            wifiRssi = -40
        )
        val resp = api.postHealth(req)
        val recorded = server.takeRequest()
        assertEquals("/api/root/v1/health", recorded.path)
        assertEquals(200, resp.code())
        assertEquals("ok", resp.body()?.status)
    }
} 