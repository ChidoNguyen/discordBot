
import sys , os



def test_pd():
# Get the parent directory
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    # Add the parent directory to sys.path
    print(os.pardir , '\n' , os.path.dirname(__file__))
    sys.path.append(parent_dir)


if __name__ == '__main__':
   test_pd()