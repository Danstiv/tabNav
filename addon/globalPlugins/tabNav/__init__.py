import addonHandler
import virtualBuffers.gecko_ia2
import oleacc
from browseMode import BrowseModeTreeInterceptor
from globalPluginHandler import GlobalPlugin

addonHandler.initTranslation()

def searchableAttribsForNodeType_decorator(func):
    def wrapper(self, nodeType):
        if nodeType == 'tab':
            return [{"IAccessible::role": [oleacc.ROLE_SYSTEM_PAGETAB]}]
        return func(self, nodeType)
    return wrapper


class GlobalPlugin(GlobalPlugin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.old_searchableAttribsForNodeType = virtualBuffers.gecko_ia2.Gecko_ia2._searchableAttribsForNodeType
        virtualBuffers.gecko_ia2.Gecko_ia2._searchableAttribsForNodeType = searchableAttribsForNodeType_decorator(virtualBuffers.gecko_ia2.Gecko_ia2._searchableAttribsForNodeType)
        BrowseModeTreeInterceptor.addQuickNav(
            'tab',
            key='y',
            nextDoc=_('moves to the next tab'),
            nextError=_('no next tab'),
            prevDoc=_('moves to the previous tab'),
            prevError=_('no previous tab'),
        )

    def terminate(self):
        virtualBuffers.gecko_ia2.Gecko_ia2._searchableAttribsForNodeType = self.old_searchableAttribsForNodeType
