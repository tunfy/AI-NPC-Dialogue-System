using System.Collections;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.UI;
using TMPro;

public class NPCChatManager : MonoBehaviour
{
    public TMP_InputField inputField;
    public TMP_Text replyText;
    public ScrollRect scrollRect;
    public string currentNPC = "chief";

    public GameObject chatPanel;
    public GameObject sendButton;
    public GameObject scrollView;

    public Slider favorabilitySlider;
    public TMP_Text favorabilityText;

    [System.Serializable]
    public class ChatRequest
    {
        public string message;
        public string npc_type;
    }

    [System.Serializable]
    public class ChatResponse
    {
        public string reply;
        public int favorability;
    }

    [System.Serializable]

    public class NPCStatusResponse
    {
        public int favorability;
    }

    public void SendMessageToNPC()
    {
        string userMessage = inputField.text;
        replyText.text +=
        "\nPlayer: " +
        inputField.text +
        "\n";

        inputField.text = "";
        ScrollToBottom();
        StartCoroutine(SendRequest(userMessage));
    }

    IEnumerator SendRequest(string userMessage)
    {
        ChatRequest requestData = new ChatRequest();

        requestData.npc_type = currentNPC;
        requestData.message = userMessage;

        string json =
            JsonUtility.ToJson(requestData);

        UnityWebRequest request =
            new UnityWebRequest(
                "http://127.0.0.1:8000/chat",
                "POST"
            );

        byte[] body =
            System.Text.Encoding.UTF8.GetBytes(json);

        request.uploadHandler =
            new UploadHandlerRaw(body);

        request.downloadHandler =
            new DownloadHandlerBuffer();

        request.SetRequestHeader(
            "Content-Type",
            "application/json"
        );

        yield return request.SendWebRequest();

        if (request.result ==
            UnityWebRequest.Result.Success)
        {
            ChatResponse response =
                JsonUtility.FromJson<ChatResponse>(
                    request.downloadHandler.text
                );

            replyText.text +=
    "\nNPC: " +
    response.reply +
    "\n";

            // 更新好感度UI
            UpdateFavorabilityUI(response.favorability);

            Debug.Log("Text Height: " + replyText.preferredHeight);
            Debug.Log("Rect Height: " + replyText.rectTransform.rect.height);

            ScrollToBottom();
        }
        else
        {
            replyText.text =
                "请求失败:" + request.error;
        }
    }

    IEnumerator GetNPCStatus()
    {
        UnityWebRequest request =
            UnityWebRequest.Get(
                "http://127.0.0.1:8000/npc_status/" + currentNPC
            );

        yield return request.SendWebRequest();

        if (request.result ==
            UnityWebRequest.Result.Success)
        {
            NPCStatusResponse response =
                JsonUtility.FromJson<NPCStatusResponse>(
                    request.downloadHandler.text
                );

            UpdateFavorabilityUI(response.favorability);
        }
        else
        {
            Debug.LogError(request.error);
        }
    }

    private void Start()
    {
        replyText.text = "=== AI NPC Chat ===\n";
        chatPanel.SetActive(false);

        inputField.gameObject.SetActive(false);
        sendButton.SetActive(false);
        scrollView.SetActive(false);
    }

    void ScrollToBottom()
    {     

        Canvas.ForceUpdateCanvases();

        scrollRect.verticalNormalizedPosition = 0f;
    }

    public void OpenChat(string npcType)
    {
        currentNPC = npcType;

        chatPanel.SetActive(true);

        inputField.gameObject.SetActive(true);
        sendButton.SetActive(true);
        scrollView.SetActive(true);

        replyText.text =
            "Talking with " + npcType + "\n\n";
        StartCoroutine(GetNPCStatus());
        Debug.Log(
       "Current NPC = " + npcType
   );
        
    }

    public void CloseChat()
    {
        chatPanel.SetActive(false);

        inputField.gameObject.SetActive(false);
        sendButton.SetActive(false);
        scrollView.SetActive(false);

        currentNPC = "";
        replyText.text = "";
        inputField.text = "";
    }

    private void Update()
    {
        if (chatPanel.activeSelf &&
            Input.GetKeyDown(KeyCode.Escape))
        {
            CloseChat();
        }
    }

    void UpdateFavorabilityUI(int value)
    {
        favorabilitySlider.value = value;
        favorabilityText.text = value + " / 100";
    }
}
