package solutions.smartsecurity.root.ui

import android.os.Bundle
import android.widget.TextView
import android.widget.Button
import androidx.appcompat.app.AppCompatActivity
import solutions.smartsecurity.root.util.PermissionHelper
import solutions.smartsecurity.root.data.HealthRepository
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

class DebugActivity : AppCompatActivity() {
    private lateinit var statusView: TextView
    private lateinit var sampleButton: Button
    private val repo = HealthRepository()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        statusView = TextView(this)
        sampleButton = Button(this).apply { text = "Sample & POST" }
        setContentView(statusView)
        addContentView(sampleButton, android.widget.FrameLayout.LayoutParams(
            android.widget.FrameLayout.LayoutParams.WRAP_CONTENT,
            android.widget.FrameLayout.LayoutParams.WRAP_CONTENT
        ))
        sampleButton.setOnClickListener { sampleAndPost() }
        if (!PermissionHelper.hasAllPermissions(this)) {
            PermissionHelper.requestAllPermissions(this, 100)
        }
    }

    private fun sampleAndPost() {
        statusView.text = "Sampling..."
        CoroutineScope(Dispatchers.Main).launch {
            val result = repo.postHealthSample("debug-device", 50, -70, -40)
            statusView.text = result.fold(
                onSuccess = { "POST Success: ${it.status}" },
                onFailure = { "POST Failed: ${it.message}" }
            )
        }
    }
} 