package com.example.syncsapp


import android.graphics.SurfaceTexture
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import android.util.Log
import android.view.TextureView
import kotlinx.android.synthetic.main.activity_camera.*

class CameraActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
    }

    private val surfaceListener = object: TextureView.SurfaceTextureListener{
        override fun onSurfaceTextureSizeChanged(
            surface: SurfaceTexture?,
            width: Int,
            height: Int
        ) {

        }

        override fun onSurfaceTextureUpdated(surface: SurfaceTexture?) = Unit

        override fun onSurfaceTextureDestroyed(surface: SurfaceTexture?) = true

        override fun onSurfaceTextureAvailable(surface: SurfaceTexture?, width: Int, height: Int) {
            Log.d("CAMERA", "textureSurface width: $width height: $height");
            openCamera();
        }
    }

    override fun onResume() {
        super.onResume()
        if (cameraView.isAvailable) {
            openCamera();
        } else {
            cameraView.surfaceTextureListener = surfaceListener;
        }
    }

    private fun openCamera() {

    }

}