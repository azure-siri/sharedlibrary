def call(Map config) {

    String artifactName = config.artifactName
    String path = config.path
    String version = config.version
	  String assetRepoName = config.assetRepoName
    
    if (! artifactName || ! path || ! version || ! assetRepoName) {
        error 'Missing parameter to pipeline!'
    }
    
   
	String jenkinsScriptsDir = '/local/jenkins/jenkins-hbo.git/scripts'
    
	node('master') {
		stage('Check if file exists in S3') {      
			fileExists(artifactName, path)
                
        }
    }
}
    
def fileExists(def artifactName,def path){
    withAWS(credentials:'s3credentials') {
	   String bucketname = 'testbucket-hbo'
	  def result = s3FindFiles bucket: bucketname, path: path, glob: artifactName
	  if (result) {
        println "File exists: " + result[0]                       
    } else {
        println "File does not exist fetching from github "
							
      }
	}
}
