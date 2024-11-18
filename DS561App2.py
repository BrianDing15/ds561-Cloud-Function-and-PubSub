from google.cloud import pubsub_v1

def main():
    
    #Set up subscription and subscription path using project and subscription ID
    subscriber_client = pubsub_v1.SubscriberClient()
    subscription_path = subscriber_client.subscription_path('ds561-project-435318', 'Project3Subscription')

    #Print and acknowledge the message from PubSub channel
    def callback(message):
        print("Message Recieved")
        print(message)

        message.ack()
        print("Acknowledged " + message.message_id)

    #Pull messages from Pub/Sub subscription
    streaming_pull_future = subscriber_client.subscribe(subscription_path, callback=callback)

    #Timeout after 2 minutes
    try:
        streaming_pull_future.result(timeout=120)
    except:
        streaming_pull_future.cancel()
        streaming_pull_future.result()

    subscriber_client.close()

if __name__ == "__main__":
    main()