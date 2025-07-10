# DefaultApi

All URIs are relative to *http://localhost*

| Method | HTTP request | Description |
| ------------- | ------------- | ------------- |
| [**apiRootV1HealthPost**](DefaultApi.md#apiRootV1HealthPost) | **POST** /api/root/v1/health | Upload health beacon sample |


<a id="apiRootV1HealthPost"></a>
# **apiRootV1HealthPost**
> HealthResponse apiRootV1HealthPost(healthRequest)

Upload health beacon sample

### Example
```kotlin
// Import classes:
//import solutions.smartsecurity.contracts.health.infrastructure.*
//import solutions.smartsecurity.contracts.health.models.*

val apiInstance = DefaultApi()
val healthRequest : HealthRequest =  // HealthRequest | 
try {
    val result : HealthResponse = apiInstance.apiRootV1HealthPost(healthRequest)
    println(result)
} catch (e: ClientException) {
    println("4xx response calling DefaultApi#apiRootV1HealthPost")
    e.printStackTrace()
} catch (e: ServerException) {
    println("5xx response calling DefaultApi#apiRootV1HealthPost")
    e.printStackTrace()
}
```

### Parameters
| Name | Type | Description  | Notes |
| ------------- | ------------- | ------------- | ------------- |
| **healthRequest** | [**HealthRequest**](HealthRequest.md)|  | |

### Return type

[**HealthResponse**](HealthResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

