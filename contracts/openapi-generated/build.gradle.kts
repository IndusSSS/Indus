plugins {
    kotlin("jvm") version "1.9.24"
}

java {
    sourceCompatibility = JavaVersion.VERSION_17
    targetCompatibility = JavaVersion.VERSION_17
}

dependencies {
    implementation(libs.moshi)
    implementation(libs.moshi.kotlin)
}

sourceSets["main"].java.srcDir("build/generated/src/main/kotlin") 