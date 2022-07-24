import org.jetbrains.kotlin.gradle.tasks.KotlinCompile

plugins {
    kotlin("jvm") version "1.6.21"
    application
}

group = "me.seongjun"
version = "1.0-SNAPSHOT"

repositories {
    maven("https://jitpack.io")
    mavenCentral()
}

dependencies {
    implementation("com.github.woowacourse-projects:mission-utils:1.0.0")
    testImplementation(kotlin("test"))
    testImplementation("io.kotest", "kotest-runner-junit5", "5.2.3")

}

tasks.test {
    useJUnitPlatform()
}

tasks.withType<KotlinCompile> {
    kotlinOptions.jvmTarget = "11"
}

application {
    mainClass.set("MainKt")
}