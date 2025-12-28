from pydantic import BaseModel, Field

class AbuseIPDBResponse(BaseModel):
    ipAddress: str = Field(..., description="The IP address being queried.")
    isValid: bool = Field(..., description="Indicates if the IP address is valid.")
    abuseConfidenceScore: int = Field(
        ..., description="Abuse confidence score from 0 to 100."
    )
    countryCode: str = Field(..., description="Country code of the IP address.")
    usageType: str = Field(..., description="Type of usage for the IP address.")

