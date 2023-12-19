from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Caminho para o ChromeDriver
chrome_driver_path = r'C:\Users\joaop\PycharmProjects\Bot_Promocao\chromedriver.exe'

# Configuração do serviço do ChromeDriver
service = Service(chrome_driver_path)

# Configuração das opções do navegador (opcional)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Para iniciar a janela do navegador maximizada

# Inicializa o navegador com as opções e o serviço
driver = webdriver.Chrome(service=service, options=options)


# Navega até o link do produto
driver.get("https://www.pichau.com.br/processador-amd-ryzen-7-5700x-8-core-16-threads-3-4ghz-4-6ghz-turbo-cache-36mb-am4-100-100000926wof")

# Espera até que o rodapé esteja presente, indicando que a página está carregada
footer_element = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, '//footer'))
)

# Aceitar os cookies se necessário
try:
    cookies_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'rcc-confirm-button'))
    )
    cookies_button.click()
except Exception as e:
    print("Erro ao tentar aceitar os cookies:", e)

# Clique no botão "Adicionar ao carrinho"
try:
    add_to_cart_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="add-to-cart"]'))
    )
    add_to_cart_button.click()
except Exception as e:
    print("Erro ao tentar adicionar ao carrinho:", e)

# Aguarde e clique no primeiro label dentro do elemento específico (não sei qual seria esse passo no seu caso)
try:
    shipping_label = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="shipping-address-item"]'))
    )
    shipping_label.click()
except Exception as e:
    print("Erro ao tentar selecionar endereço de envio:", e)

# Clique no botão para continuar para o pagamento
try:
    continue_to_payment = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="address-continue-to-payment"]'))
    )
    continue_to_payment.click()
except Exception as e:
    print("Erro ao tentar prosseguir para o pagamento:", e)

# Clique na div específica de método de pagamento
try:
    payment_method = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, 'payment-method-mercadopago_custom_pix'))
    )
    payment_method.click()
except Exception as e:
    print("Erro ao tentar selecionar o método de pagamento:", e)

# Continue para revisão
try:
    continue_to_review = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="payment-continue-to-review"]'))
    )
    continue_to_review.click()
except Exception as e:
    print("Erro ao tentar prosseguir para a revisão:", e)

# Marque o checkbox
try:
    checkbox = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[type="checkbox"]'))
    )
    checkbox.click()
except Exception as e:
    print("Erro ao tentar marcar o checkbox:", e)

# Finalize o pedido
try:
    finalize_order_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-cy="finalize-order"]'))
    )
    finalize_order_button.click()
except Exception as e:
    print("Erro ao tentar finalizar o pedido:", e)
