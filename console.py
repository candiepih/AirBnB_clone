#!/usr/bin/python3
"""
AirBnB clone - The console
"""
import cmd
import re
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import models
model_names = ['BaseModel', 'User', 'Place',
               'State', 'City', 'Amenity', 'Review']
number_args = ['number_rooms', 'number_bathrooms',
               'max_guest', 'price_by_night']
float_args = ['latitude', 'longitude']


class HBNBCommand(cmd.Cmd):
    """AirBnB - The console"""
    prompt = "(hbnb) "

    def emptyline(self):
        """Print an empty line"""
        pass

    def do_all(self, cls_name):
        """Prints all str repr of all instances of class name"""
        str_list = []
        if not cls_name:
            for v in storage.all().values():
                str_list.append(str(v))
        else:
            if cls_name not in model_names:
                print("** class doesn't exist **")
                return
            for k, v in storage.all().items():
                left = k.split('.')[0]
                if left == cls_name:
                    str_list.append(str(v))
        print(str_list)

    def do_show(self, args):
        """Prints the string representation of an instance"""
        data = args.split()

        if len(data) == 0:
            return print("** class name missing **")
        if data[0] not in model_names:
            return print("** class doesn't exist **")
        if len(data) == 1:
            return print("** instance id missing **")
        try:
            eval(data[0])
        except Exception:
            return print("** class doesn't exist **")

        objDict = storage.all()
        keyId = data[0] + "." + data[1]

        try:
            value = objDict[keyId]
            print(value)
        except KeyError:
            print("** no instance found **")

    def do_create(self, args):
        """Creates a new instance"""
        if len(args) == 0:
            return print("** class name missing **")
        data = args.split()

        try:
            newInstance = eval(data[0])()
            newInstance.save()
            print(newInstance.id)
        except Exception:
            print("** class doesn't exist **")

    def do_update(self, args, isdict=False):
        """Updates an instance based on the class name and ID"""

        if not args:
            return print("** class name missing **")

        data = args.split()
        remove_chars = '['+'"\''+']'

        if isdict:
            keys = []
            values = []

            for i in range(len(data)):
                if i <= 1:
                    continue
                if i % 2 == 0:
                    keys.insert(i, data[i].strip('"'))
                else:
                    key = data[i-1].strip('"')
                    val = data[i].strip('"')
                    if key in number_args:
                        val = int(val)
                    if key in float_args:
                        val = float(val)
                    values.insert(i, val)
            dict_data = dict(zip(keys, values))

        if data[0] not in model_names:
            print("** class doesn't exist **")
        elif len(data) == 1:
            print("** instance id missing **")
        else:
            all_objs = storage.all()
            for key, val in all_objs.items():
                ob_name = val.__class__.__name__
                ob_id = val.id
                if (ob_name == data[0] and
                        ob_id == re.sub(remove_chars, '', data[1])):
                    if len(data) == 2:
                        return print("** attribute name missing **")
                    elif len(data) == 3:
                        return print("** value missing **")
                    else:
                        if isdict:
                            for key in dict_data:
                                setattr(val, key, dict_data[key])
                                storage.save()
                        else:
                            value = re.sub(remove_chars, '', data[3])
                            if "'" not in data[3] and '"' not in data[3]:
                                try:
                                    value = int(value)
                                except Exception:
                                    try:
                                        value = float(value)
                                    except Exception:
                                        pass

                            setattr(
                                val, re.sub(
                                    remove_chars, '', data[2]), value)
                            storage.save()
                    return
            print("** no instance found **")

    def do_destroy(self, args):
        """Deletes an instance based on the class name and ID"""
        # if not args:
        #     return print("** class name missing **")

        data = args.split()

        if len(args) == 0:
            return print("** class name missing **")
        if data[0] not in model_names:
            return print("** class doesn't exist **")
        if len(data) == 1:
            return print("** instance id missing **")

        try:
            eval(data[0])
        except Exception:
            return print("** class doesn't exist **")
        objDict = storage.all()
        keyId = data[0] + "." + data[1]

        try:
            del objDict[keyId]
        except Exception:
            return print("** no instance found **")
        storage.save()

    def default(self, args):
        """Default (fallback) Function"""
        arg = args.split(".")
        if arg[0] not in model_names:
            return print("** class doesn't exist **")
        if len(arg) > 1:
            if arg[1] == "all()":
                self.do_all(arg[0])
            if arg[1] == "count()":
                sum = 0
                for key, val in models.storage.all().items():
                    if arg[0] in key:
                        sum += 1
                print(sum)
            if "show" in arg[1]:
                # if '"' not in arg[1] or '()' in arg[1] or '("")' in arg[1]:
                #     return print("** instance id missing **")
                self.do_show(arg[0] + " " + arg[1].split('"')[1])
            if "update" in arg[1]:
                remove_chars = '['+'"\':,})'+']'
                try:
                    if '{' in arg[1] and '}' in arg[1]:
                        sparg = arg[1].split('{')
                        id = sparg[0].split('"')[1]
                        data = re.sub(remove_chars, '', sparg[1])

                        self.do_update(arg[0] + ' ' + id + ' ' + data, True)
                    else:
                        data = re.sub(remove_chars, '',
                                      arg[1].replace('update(', ''))

                        self.do_update(arg[0] + ' ' + data)
                except Exception:
                    print("** attribute is missing **")
            if "destroy" in arg[1]:
                # if '"' not in arg[1] or '()' in arg[1] or '("")' in arg[1]:
                #     return print("** instance id missing **")
                self.do_destroy(arg[0] + " " + arg[1].split('"')[1])

    def do_EOF(self, args):
        """End Of File"""
        return True

    def do_quit(self, args):
        """Quit command to exit the program"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
