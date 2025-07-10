plugins {
    id("com.android.application")
    kotlin("android")
}

android {
    namespace = "solutions.smartsecurity.root"
    compileSdk = 34

    defaultConfig {
        applicationId = "solutions.smartsecurity.root"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "0.1"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        getByName("release") {
            isMinifyEnabled = false
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}

dependencies {
    implementation(libs.retrofit)
    implementation(libs.retrofit.moshi)
    implementation(libs.okhttp)
    implementation(libs.moshi)
    implementation(libs.work.runtime)
    implementation(project(":contracts:openapi-generated"))
} 