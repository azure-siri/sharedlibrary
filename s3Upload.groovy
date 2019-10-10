def call(Map config) {

    String artifactName = config.artifactName
    String path = config.path
    String version = config.version
	  String assetRepoName = config.assetRepoName
    
    if (! artifactName || ! path || ! version || ! assetRepoName) {
        error 'Missing parameter to pipeline!'
    }
    
    String bucketname = 'testbucket-hbo'
	String jenkinsScriptsDir = '/local/jenkins/jenkins-hbo.git/scripts'
    
    pipeline {
        agent any
		    stages {
			    stage('Check if file exists in S3') {      
				    steps {
					fileExists(artifactName, path)
                
            }
          }
        }
    }
}

def fileExists(artifactName, path){
    withAWS(credentials:'s3credentials') {
	  def result = s3FindFiles bucket: bucketname, path: path, glob: artifactName
	  if (result) {
        println "File exists: " + result[0]                       
    } else {
        println "File does not exist fetching from github "
							
      }
	}
}
