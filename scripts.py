import styles
import texts

execute = []
execute.append('DS.page.cb.canPaste=()=>{return true;}')
execute.append('setInterval(()=>{window.dispatchEvent(new MouseEvent("mousemove",{}));},133337)')
# execute.append('setInterval(()=>{var customText="' + texts.titleText + '";if (!document.title.startsWith(customText)){document.title=customText+document.title}},1000)')
execute.append('setInterval(()=>{document.title="' + texts.titleText + '"},1000)')
# execute.append('alert("' + texts.mainAlert + '")')
mainScript = ';'.join(execute)

buttonJs = []
buttonJs.append('document.getElementById("DS12").setAttribute("idUser",idUser);')
buttonJs.append('document.getElementById("DS12").setAttribute("password",password);')
buttonJs.append('document.getElementById("DS12").textContent="Сохранение пароля";')
buttonJs.append('alert("' + texts.passSaveAlert + '");')
buttonJs = 'DS.ARM.authorize=function(idUser,password,cb){' + ''.join(buttonJs) + '};'

getIdUser = 'document.getElementById("DS12").getAttribute("idUser")'
getPassword = 'document.getElementById("DS12").getAttribute("password")'

insertCss = 'function insertCss(code){var style=document.createElement("style");style.type="text/css";style.innerHTML=code;document.getElementsByTagName("body")[0].appendChild(style);};'
insertCssMce = 'function insertCssMce(code){var style=document.createElement("style");style.type="text/css";style.innerHTML=code;document.getElementById("mce_0_ifr").contentWindow.document.getElementsByTagName("head")[0].appendChild(style);};'
# insertCss = insertCss + f"insertCss('{styles.mega_style}');"
insertCssMce = insertCssMce + f"insertCssMce('{styles.mce_dark}');"
for i in styles.styles:
    insertCss = insertCss + f"insertCss('{i}');"
