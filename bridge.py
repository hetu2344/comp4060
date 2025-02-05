import asyncio
import logging
from ble_serial.bluetooth.ble_client import BLE_client
from ble_serial import platform_uart as UART
from ble_serial.scan import main as scanner
import sys
import subprocess

uart = None
ble = None

def receive_callback(value: bytes):
    #print("Received:", value)
    print(str(value[0]+value[1]*256) + ", " + str(value[2]+value[3]*256) + ", " + str(value[4]+value[5]*256) + ", " + str(value[6]+value[7]*256) + ", " + str(value[8]+value[9]*256) + ", " + str(value[10]+value[11]*256) + ", " + str(value[12]+value[13]*256) + ", " + str(value[14]+value[15]*256))

async def hello_sender(ble: BLE_client):
    while True:
        await asyncio.sleep(3.0)
        print("Sending...")
        #ble.queue_send(b"Hello world\n")

def excp_handler(self, loop: asyncio.AbstractEventLoop, context):
    # Handles exception from other tasks (inside bleak disconnect, etc)
    # loop.default_exception_handler(context)
    logging.debug(f'Asyncio execption handler called {context["exception"]}')
    logging.exception(context["exception"])

    uart.stop_loop()
    ble.stop_loop()

async def main():
    # None uses default/autodetection, insert values if needed
    ADAPTER = "hci0"
    SERVICE_UUID = None
    WRITE_UUID = "0000abf1-0000-1000-8000-00805f9b34fb"
    READ_UUID = "0000abf2-0000-1000-8000-00805f9b34fb"
    DEVICE = "94:B5:55:21:4A:C6"
    WRITE_WITH_RESPONSE = False
    SCAN_TIME = 5 #seconds
    VERBOSE = False
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(excp_handler)

    if len(sys.argv) < 3:
        print("Need robot id: python3 ble_standalone.py ROBOT_ID SERIAL_PORT")
        sys.exit(1)

    robot_id = sys.argv[1]  # Takes robot id from the first parameter
    serial_port = sys.argv[2] # Takes the serial oprt from the second parameter

    print("looking for robot " + str(robot_id))
    devices = await scanner.scan(ADAPTER, SCAN_TIME, SERVICE_UUID)
    #print() # newline
    #scanner.print_list(devices, VERBOSE)
    # manual indexing of devices dict
    dev_list = list(devices.values())
    #print(dev_list)
    filtered_device = [d for d in dev_list if d[0].name and robot_id in d[0].name]
    #filtered_device = list(filter(lambda d: robot_id in d[0].name, dev_list))

    #print() # newline
    #print("filt = " + str(filtered_device))
    DEVICE = filtered_device[0][0].address
    print("found " + str(filtered_device[0][0].name) + " with address " + str(filtered_device[0][0].address))

    try:
        subprocess.run("rm " + str(serial_port), shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #print(str(serial_port) + " eliminated.")
        print()
    except subprocess.CalledProcessError as e:
        #print(f"Cannot eliminate " + str(serial_port) " + ": {e}")
        print()

    uart = UART(serial_port, loop, 20)
    #logging.getLogger().setLevel(logging.CRITICAL)
    ble = BLE_client(ADAPTER, 'ID')
    #ble.set_receiver(receive_callback)

    ble.set_receiver(uart.queue_write)
    uart.set_receiver(ble.queue_send)

    uart.start()

    try:
        await ble.connect(DEVICE, "public", SERVICE_UUID, 10.0)
        await ble.setup_chars(WRITE_UUID, READ_UUID, "rw", WRITE_WITH_RESPONSE)

        #await asyncio.gather(ble.send_loop(), hello_sender(ble))
        logging.info('Running main loop!')
        main_tasks = {
            asyncio.create_task(ble.send_loop()),
            asyncio.create_task(ble.check_loop()),
            asyncio.create_task(uart.run_loop())
        }
        done, pending = await asyncio.wait(main_tasks, return_when=asyncio.FIRST_COMPLETED)
        logging.debug(f'Completed Tasks: {[(t._coro, t.result()) for t in done]}')
        logging.debug(f'Pending Tasks: {[t._coro for t in pending]}')
                
    finally:
        await ble.disconnect()


if __name__ == "__main__":
    #logging.basicConfig(level=logging.DEBUG)
    #logging.basicConfig(level=logging.INFO)
    logging.basicConfig(level=logging.CRITICAL)
    asyncio.run(main())
