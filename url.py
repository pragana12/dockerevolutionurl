from playwright.sync_api import sync_playwright, expect
import re
import time
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
USER_LOGIN = os.getenv('USER_LOGIN')
SENHA_LOGIN = os.getenv('SENHA_LOGIN')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)



# Função para Salvar url no sapabase
def save_url_supabase(url):

    try:
        result = (supabase.table('websocketurl')
                .update({'url': url})
                .eq('id', '1')
                .execute())
        
        if result.data:
            print(f'URL salva no Supabase com sucesso: {url}')
        else:
            print('Nenhum registro foi atualizado')
            
    except Exception as e:
        print(f'Erro ao salvar URL no Supabase: {str(e)}')

def esportedasorte():
    # Função para capturar e imprimir a URL do WebSocket
    def log_ws_requests(ws):
        if ws.url.startswith("wss://esportesdasorte.evo-games.com/public/roulette/player/game/") and "messageFormat=json" in ws.url:
            # Substituir a parte da URL por {id_roleta}
            modified_url = re.sub(r"(game/)[^/]+(/socket)", r"\1{id_roleta}\2", ws.url)
            print(f"WS Request URL: {modified_url}")

            url = modified_url
            save_url_supabase(url)
            return modified_url  # Retorna a URL do WebSocket
        

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Intercepta as requisições WebSocket
        page.on('websocket', log_ws_requests)

        # Navega para a página desejada
        page.goto("https://www.esportesdasorte.com/ptb/bet/main")
        print('Abriu o esporte da sorte')
        expect(page.get_by_role("button", name="Login")).to_be_visible(timeout=60000)
        page.get_by_role("textbox", name="Usuário").click()
        page.get_by_role("textbox", name="Usuário").fill(USER_LOGIN)
        page.get_by_role("textbox", name="Senha").click()
        page.get_by_role("textbox", name="Senha").fill(SENHA_LOGIN)
        page.get_by_role("button", name="Login").click()
        expect(page.get_by_role("button", name="Login")).not_to_be_visible(timeout=60000)
        print('fez o login')
        page.goto("https://www.esportesdasorte.com/ptb/games/livecasino/detail/normal/18451/evol_XxxtremeLigh0001_BRL")
        print('entrou na roleta')
        time.sleep(10)
        # Tira uma captura de tela e salva no arquivo 'screenshot.png'
        page.screenshot(path="./screenshot.png")


        # Mantém o navegador aberto por algum tempo para capturar as requisições WebSocket
        page.wait_for_timeout(10000)  # Espera 10 segundos (10000 ms)

        browser.close()

if __name__ == "__main__":
    while True:
        esportedasorte()
        time.sleep(600)