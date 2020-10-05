# python examples for consumers and producers 


sqs script: 

    usage: 
        
        [--nodeRoleName NODEROLENAME]  
        [--sqsQueueUrl SQSQUEUEURL]
        [--bootstrapServers BOOTSTRAPSERVERS]
        [--schemaRegistry SCHEMAREGISTRY]
        [--topicName TOPICNAME]

    run: 
        <python sqsProducer.py --nodeRoleName="admin" --sqsQueueUrl='test_query' --bootstrapServers='localhost:9092' --schemaRegistry='http://localhost:8081' --topicName='psi-granule-input-unknown'>
