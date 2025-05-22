import asyncio
import webview
import edge_tts

def on_loaded():
    print("Окно загружено!")

def speak_text(text):
    async def speak(text, voice="ru-RU-DmitryNeural", output_file="output.mp3"):
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file)
        return output_file
    
    try:
        output_file = asyncio.run(speak(text))
        return {
            'success': True,
            'message': f"Текст успешно озвучен и сохранен как {output_file}",
            'file': output_file
        }
    except Exception as e:
        return {
            'success': False,
            'message': f"Ошибка озвучки: {str(e)}",
            'file': None
        }

html = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
    <title>Озвучивание текста</title>
    <style>
      .centered-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        min-height: 80vh;
        gap: 1.5rem;
        padding-top: 2rem;
      }
      .input-group {
        width: 100%;
        max-width: 400px;
      }
      button.centered {
        width: 100%;
        max-width: 400px;
      }
      h1 {
        margin-bottom: 5rem;
      }
      #result {
        margin-top: 2rem;
        padding: 1rem;
        border-radius: 0.5rem;
        max-width: 400px;
        width: 100%;
        text-align: center;
      }
      .success {
        background-color: #d1fae5;
        color: #065f46;
        border: 1px solid #a7f3d0;
      }
      .error {
        background-color: #fee2e2;
        color: #b91c1c;
        border: 1px solid #fecaca;
      }
      .processing {
        background-color: #e0e7ff;
        color: #4338ca;
        border: 1px solid #c7d2fe;
      }
    </style>
  </head>
  <body>
    <main class="container">
      <div class="centered-container">
        <h1>Озвучивание текста</h1>
        <div class="input-group">
            <input type="text" id="text-input" name="text-input" placeholder="Введите текст для озвучки...">
        </div>
        <button type="button" class="primary centered" onclick="handleSpeakButton()">Озвучить</button>
        <div id="result" style="display: none;"></div>
      </div>
      <div style="position: absolute; bottom: 20px; right: 20px; font-family: 'Segoe UI'; font-weight: bold; padding: 10px;"> LLP, ins </div>
    </main>

    <script>
      async function handleSpeakButton() {
        const text = document.getElementById('text-input').value;
        const resultDiv = document.getElementById('result');
        
        if (!text) {
          resultDiv.innerText = "Пожалуйста, введите текст для озвучки";
          resultDiv.className = "error";
          resultDiv.style.display = "block";
          return;
        }
        
        try {
          resultDiv.innerText = "Идет процесс озвучки... Пожалуйста, подождите. (Помните, чем больше текст, тем дольше создаётся озвучка)";
          resultDiv.className = "processing";
          resultDiv.style.display = "block";
          
          const response = await window.pywebview.api.speak_text(text);
          
          resultDiv.innerText = response.message;
          resultDiv.className = response.success ? "success" : "error";
          
        } catch (e) {
          resultDiv.innerText = "Произошла ошибка: " + e;
          resultDiv.className = "error";
        }
      }
    </script>
  </body>
</html>
"""


window = webview.create_window(
    title="Озвучивание текста",
    html=html,
    width=800,
    height=600
)

window.expose(speak_text)
webview.start()