using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Diagnostics;

public class BackendLauncher : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        Process.Start(
            "cmd.exe",
            "/k cd /d C:\\Users\\lenovo\\Desktop\\AI-NPC-Project\\backend && venv\\Scripts\\uvicorn.exe main:app --reload");
    }

}
