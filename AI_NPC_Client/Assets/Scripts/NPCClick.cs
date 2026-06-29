using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class NPCClick : MonoBehaviour
{
    public string npcType;

    private void OnMouseDown()
    {
        NPCChatManager chatManager =
            FindObjectOfType<NPCChatManager>();

        chatManager.OpenChat(npcType);
    }
}
