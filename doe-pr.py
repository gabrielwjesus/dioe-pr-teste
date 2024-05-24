from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.imprensaoficial.pr.gov.br/"
checkbox_id = "diarioCodigo8"
data_inicial_id = "dataInicialEntrada"
data_final_id = "dataFinalEntrada"
submit_button_name = "submit"
xpath_texto = '/html/body/div[1]/div/section/div/section/div/div[2]/div/div/div/section/div/form/div/div[1]/input[2]'
texto = '"Policia Cientifica"'
xpath_sem_diario = '/html/body/table/tbody/tr/td[4]/table[2]/tbody/tr/td/table/tbody/tr[3]/td/table/tbody/tr/td/table[2]/tbody/tr/td/table/tbody/tr/td'
xpath_captcha = '//*[@id="dv_aba1"]/table[1]/tbody/tr/td[2]/table[2]/tbody/tr/td/table/tbody/tr/td[1]'
    
while True:
    data_hoje = datetime.date.today()
    amanha = data_hoje + datetime.timedelta(days = 1)
    data_formatada = amanha.strftime("%d/%m/%Y")
    
    driver = webdriver.Chrome()
    driver.get(url)
    
    sleep(10)
    try:
        checkbox = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, checkbox_id)))
        checkbox.click()
        
        # Inserir datas nas caixas de texto
        data_inicial_campo = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, data_inicial_id)))
        data_inicial_campo.send_keys(data_formatada)
        
        data_final_campo = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, data_final_id)))
        data_final_campo.send_keys(data_formatada)
        
        inserir_texto = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, xpath_texto)))
        inserir_texto.send_keys(texto)    
        
        # Clicar no botão de envio
        submit_button = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.NAME, submit_button_name)))
        submit_button.click()
        
        handles = driver.window_handles
        if len(handles) > 1:
            driver.switch_to.window(handles[1])
            
            try:
                mensagem_sem_diario = driver.find_element(By.XPATH, xpath_sem_diario)
                mensagem = mensagem_sem_diario.text
                print(mensagem)
                if mensagem == "Não encontramos diários oficiais para sua consulta.":
                    print("Não há novos diários para a data de amanhã")
                    driver.quit()
            except:
                try:
                    mensagem_captcha = driver.find_element(By.XPATH, xpath_captcha)
                    captcha = mensagem_captcha.text
                    print(captcha)
                    if captcha == "Digite o texto:":
                        print("Página solicitou captcha, vamos aguardar!")
                        driver.quit()
                except:
                    print("ALERTA: Novo diário para amanhã foi encontrado!")
                    driver.quit()
                    break
                    
        else:
            print("Não há nenhuma aba adicional aberta") 
        
        
        hora_atual = datetime.datetime.now()
        #horario entre 01:00 e 23:00
        if hora_atual.strftime('%H:%M') > '01:00' and hora_atual.strftime('%H:%M') < '23:00':
            print('Aguardando 120 minutos antes da próxima tentativa')
            sleep(120*60)
        #horario de interesse entre 23:00 até 01:00
        else:
            print("Aguardando 10 minutos antes da próxima tentativa")
            sleep(10*60)
    
    except:
        print("Erro no site")
        driver.quit()
        
#driver.quit()

# (Opcional) Abrir uma nova aba com a página de resultados
# new_window_handle = driver.window_handles[-1]
# driver.switch_to.window(new_window_handle)
