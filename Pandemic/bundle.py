# encoding: utf-8
import io
import os
import shutil
import subprocess
import sys


def _run(*args):
    kwargs = {}
    if sys.version_info.major >= 3:
        # kwargs['text'] = True
        kwargs['universal_newlines'] = True
    return subprocess.check_output(args, **kwargs)


class BundleActioner(object):

    def __init__(self):
        pass

    def clone(self, source, name):
        raise NotImplementedError("Abstract bundle source")

    def update(self):
        raise NotImplementedError("Abstract bundle source")

    def remove(self, name):
        shutil.rmtree(name)
        return ""


class BundleGit(BundleActioner):

    def clone(self, source, name):
        return _run('git', 'clone', source, name)

    def update(self):
        return _run('git', 'pull')


class BundleHg(BundleActioner):

    def clone(self, source, name):
        return _run('hg', 'clone', source, name)

    def update(self):
        return _run('hg', 'pull')


class BundleLocal(BundleActioner):

    def clone(self, source, name):
        outmsg = subprocess.check_output(['cp', '-R', source, name])
        filename = os.path.join(name, '.source')
        with io.open(filename, mode='r', encoding='utf-8') as f:
            f.write(source)
        return outmsg

    def update(self):
        filename = '.source'
        with io.open(filename, mode='r', encoding='utf-8') as f:
            source = f.read()
        name = os.path.split(os.getcwd())[1]
        os.chdir(os.path.split(os.getcwd())[0])
        return self.clone(source, name)


class BundleScript(BundleActioner):

    def clone(self, source, name):
        return _run('cp', '-R', source, name)

    def update(self):
        return _run('./.update')


actioners = {
    'git': BundleGit,
    'hg': BundleHg,
    'local': BundleLocal,
    'script': BundleScript,
}


class Bundle(object):

    def __init__(self, name, source, btype, bdir, printer):
        self.printer = printer
        self.name = name
        self.bdir = os.path.expanduser(bdir)
        self.source = source
        self.btype = btype
        self.bname = self.__findbundle()
        self.actioner = actioners[btype]()

    def clone(self):
        # clone from whatever repository or whatever
        self.__savecwd()
        os.chdir(self.bdir)

        if self.bname is not None:
            # path already exists
            # best action to take is probably to just remove and clone
            # XXX: this isn't safe, though :(
            self.printer.warn("%s exists!" % (self.bname))
            self.remove()

        msg = self.actioner.clone(self.source, self.name)
        self.printer.message(msg)

        self.__restorecwd()

    def remove(self):
        # delete an existing bundle directory
        self.__savecwd()
        os.chdir(self.bdir)

        if self.bname is not None:
            msg = self.actioner.remove(self.bname)
            self.printer.message(msg)
        else:
            self.printer.warn("%s doesn't exist!" % (self.name))

        self.__restorecwd()

    def update(self):
        # update a repository
        self.__savecwd()
        os.chdir(self.bdir)

        if self.bname is not None:
            os.chdir(self.bname)
            msg = self.actioner.update()
            self.printer.message(msg)
        else:
            self.printer.warn("%s doesn't exist!" % (self.name))
            self.clone()

        self.__restorecwd()

    def __findbundle(self):
        orig = os.path.join(self.bdir, self.name)
        disabled = os.path.join(self.bdir, "%s~" % self.name)

        if os.path.exists(orig):
            return self.name
        elif os.path.exists(disabled):
            self.printer.warn("Using disabled form of %s..." % self.name)
            return "%s~" % self.name
        else:
            return None

    def __savecwd(self):
        self.__lastcwd = os.getcwd()

    def __restorecwd(self):
        os.chdir(self.__lastcwd)
