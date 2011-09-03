from pili import lite
from gettext import NullTranslations
import pystache
import time

class pilii18n(NullTranslations):
    def gettext(text):
        echo(text + "#")


def ha():
    return 'girvan'

def i18n(text):
    return lambda text: "#"+text+"#"
def main():
    lite.init(globals())
    html = I18nIndex(wife='linda', i18n=i18n).render()
    echo(html)

class I18nIndex(pystache.View):
    template_path = '../tpls'
    def thing(self):
        return ha()
    def ld(self, text):
        return lambda text: "#" + text + "#"

if __name__ == '__main__':
    main()
