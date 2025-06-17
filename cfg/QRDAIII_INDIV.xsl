<!-- Title: CDA XSL StyleSheet Original Filename: cda.xsl  Version: 3.0 Revision History: 08/12/08 Jingdong Li updated Revision History: 12/11/09 KH updated  Revision History:  03/30/10 Jingdong Li updated. Revision History:  08/25/10 Jingdong Li updated Revision History:  09/17/10 Jingdong Li updated Revision History:  01/05/11 Jingdong Li updated Specification: ANSI/HL7 CDAR2 The current version and documentation are available at http://www.lantanagroup.com/resources/tools/.  We welcome feedback and contributions to tools@lantanagroup.com The stylesheet is the cumulative work of several developers; the most significant prior milestones were the foundation work from HL7  Germany and Finland (Tyylitiedosto) and HL7 US (Calvin Beebe), and the presentation approach from Tony Schaller, medshare GmbH provided at IHIC 2009. 
-->
<!-- LICENSE INFORMATION Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0 
-->

<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:sdtc="urn:hl7-org:sdtc"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xmlns="urn:hl7-org:v3"
  xmlns:voc="urn:hl7-org:v3/voc">
  <xsl:output method="xml" indent="yes" omit-xml-declaration="yes" version="4.01" encoding="ISO-8859-1" doctype-system="http://www.w3.org/TR/html4/strict.dtd" doctype-public="-//W3C//DTD HTML 4.01//EN"/>
  <!-- global variable title -->

  <!--<xsl:variable name="title"> <xsl:choose>  <xsl:when test="string-length(/ClinicalDocument/title) &gt;= 1"> <xsl:value-of select="/ClinicalDocument/title"/>  </xsl:when>  <xsl:when test="/ClinicalDocument/code/@displayName"> <xsl:value-of select="/ClinicalDocument/code/@displayName"/>  </xsl:when>  <xsl:otherwise> <xsl:text>Clinical Document</xsl:text>  </xsl:otherwise> </xsl:choose>  </xsl:variable>-->

  <!-- Main -->
  <xsl:template match="/">
    <ClinicalDocument >
      <xsl:apply-templates select="QRDA"/>
    </ClinicalDocument>
  </xsl:template>
  <!-- produce browser rendered, human readable clinical document -->
  <xsl:template match="QRDA">
    <!-- QRDA Header -->
    <realmCode code="US"/>
    <typeId root="2.16.840.1.113883.1.3" extension="POCD_HD000040"/>
    <templateId root="2.16.840.1.113883.10.20.27.1.1" extension="2016-06-01"/>
    <templateId root="2.16.840.1.113883.10.20.27.1.2" extension="2024-12-01"/>
    <id root="26a42253-99f5-48e7-9274-b467c6c7f623"/>
    <code code="55184-6" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Quality Reporting Document Architecture Calculated Summary Report"/>
    <title>eCQMs</title>
    <confidentialityCode codeSystem="2.16.840.1.113883.5.25" code="N"/>
    <languageCode code="en" />
    <setId root="ae23711d-783d-4f5e-b942-4084b467848b"/>
    <versionNumber value="1"/>
    <recordTarget>
      <patientRole>
        <id nullFlavor="NA"/>
      </patientRole>
    </recordTarget>
    <!-- This is the document creation time -->
    <effectiveTime>
      <xsl:attribute name="value">
        <xsl:value-of select="documentGeneratedDatetime"></xsl:value-of>
      </xsl:attribute>
    </effectiveTime>
    <languageCode code="eng"/>

    <informationRecipient>
      <intendedRecipient>
        <id root="2.16.840.1.113883.3.249.7" extension="MIPS_INDIV"/>
      </intendedRecipient>
    </informationRecipient>

    <participant typeCode="DEV">
      <associatedEntity classCode="RGPR">
        <!-- CMS EHR Certification Number  -->
        <id root="2.16.840.1.113883.3.2074.1" extension="0015HBC1D1EFG1H"/>
      </associatedEntity>
    </participant>

    <!-- START display top portion of clinical document -->
    <xsl:call-template name="author"/>
    <xsl:call-template name="custodian"/>
    <xsl:call-template name="legalAuthenticator"/>
    <xsl:call-template name="documentationOf"/>
    <!-- Hard coded for now-->
    <component>
      <structuredBody>
        <xsl:call-template name="MeasureSection"/>
        <xsl:call-template name="ReportingParameters"/>
      </structuredBody>
    </component>

    <!-- END display top portion of clinical document -->
  </xsl:template>


  <xsl:template name="labresultsPerformed">
    <xsl:for-each select="/QRDA/resultListObj/Result">
      <entry>
        <observation classCode="OBS" moodCode="EVN">
          <!-- Lab test performed -->
          <templateId root="2.16.840.1.113883.10.20.24.3.38" extension="2016-02-01"/>
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>

          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="conceptCodeOID" />
            <xsl:with-param name="code" select="conceptValue" />
            <xsl:with-param name="valueset" select="conceptValueOID" />
            <xsl:with-param name="sectiontype" select="'labtestorder'" />
            <xsl:with-param name="text" select="codeDisplayName" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>

          <!--<code>
            <xsl:if test="boolean(codeSystem) and (codeSystem != '')">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="codeSystem"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:attribute name="code">
              <xsl:value-of select="codeCode"/>
            </xsl:attribute>
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="codeDisplayName"/>
            </originalText>
          </code>-->

          <text>
            <xsl:value-of select="codeDisplayName"/>
          </text>
          <statusCode code="completed" />

          <effectiveTime>
            <low>
              <xsl:if test="effectiveTime != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTime"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTime = '' or boolean(effectiveTime) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTime != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTime"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTime = '' or boolean(effectiveTime) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <xsl:for-each select="resultObs/ResultObs">


            <xsl:choose>
              <xsl:when test ="(boolean(valueCode)) and valueCode != ''">
                <value xsi:type="CD">
                  <xsl:if test="boolean(valueCodeValueSet) and (valueCodeValueSet != '')">
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="valueCodeValueSet"/>
                    </xsl:attribute>
                  </xsl:if>

                  <xsl:attribute name="code">
                    <xsl:value-of select="valueCode"/>
                  </xsl:attribute>
                  <xsl:if test="valueCodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="valueCodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="valueCodeSystem = ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="valueValue != ''">
                    <originalText>
                      <xsl:value-of select="valueValue"/>
                    </originalText>
                  </xsl:if>
                </value>
              </xsl:when>
              <xsl:when test ="((boolean(valueCode)) and valueCode = '') or boolean(valueCode) = false">
                <xsl:choose>
                  <xsl:when test ="(boolean(valueValue)) and valueValue != ''">
                    <value xsi:type="ST">
                      <xsl:value-of select="valueValue"/>
                    </value>
                  </xsl:when>
                  <xsl:otherwise>
                    <value xsi:type="CD" nullFlavor="UNK" />
                  </xsl:otherwise>
                </xsl:choose>
              </xsl:when>
              <xsl:otherwise>
                <value xsi:type="CD" nullFlavor="UNK" />
              </xsl:otherwise>
            </xsl:choose>


            <!--<xsl:if test="valueCode != ''">
              <value xsi:type="CD">
                <xsl:if test="boolean(valueCodeValueSet) and (valueCodeValueSet != '')">
                  <xsl:attribute name="sdtc:valueSet">
                    <xsl:value-of select="valueCodeValueSet"/>
                  </xsl:attribute>
                </xsl:if>

                <xsl:attribute name="code">
                  <xsl:value-of select="valueCode"/>
                </xsl:attribute>
                <xsl:if test="valueCodeSystem != ''">
                  <xsl:attribute name="codeSystem">
                    <xsl:value-of select="valueCodeSystem"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="valueCodeSystem = ''">
                  <xsl:attribute name="codeSystem">
                    <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="valueValue != ''">
                  <originalText>
                    <xsl:value-of select="valueValue"/>
                  </originalText>
                </xsl:if>
              </value>
            </xsl:if>

            <xsl:if test="valueCode = ''">
              <xsl:if test="valueValue != ''">
                <value xsi:type="ST">
                  <xsl:value-of select="valueValue"/>
                </value>
              </xsl:if>
            </xsl:if>
            
            <xsl:if test="valueCode = '' and valueValue = ''">
              <value xsi:type="CD" nullFlavor="UNK" />
            </xsl:if>-->

            <!--<xsl:choose>
              <xsl:when test="valuetype='PQ'">
                <value xsi:type="PQ">
                  <xsl:attribute name="value">
                    <xsl:value-of select="valueValue"/>
                  </xsl:attribute>
                  <xsl:if test="boolean(valueUnit) and (valueUnit != '')">
                    <xsl:attribute name="unit">
                      <xsl:value-of select="valueUnit"/>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </xsl:when>
              <xsl:when test="valuetype='CD'">
                <xsl:if test="code != ''">
                  <value xsi:type="CD">
                    <xsl:attribute name="code">
                      <xsl:value-of select="code"/>
                    </xsl:attribute>
                    <xsl:if test="valueCodeSystem != ''">
                      <xsl:attribute name="codeSystem">
                        <xsl:value-of select="valueCodeSystem"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="boolean(valueCodeSystem) or (valueCodeSystem = '')">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:if>
                    <xsl:if test="displayName != ''">
                      <originalText>
                        <xsl:value-of select="displayName"/>
                      </originalText>
                    </xsl:if>
                  </value>
                </xsl:if>
              </xsl:when>
              <xsl:when test="valuetype='ST'">
                <value xsi:type="ST">
                  <xsl:value-of select="valueValue"/>
                </value>
              </xsl:when>
              <xsl:otherwise>
                <xsl:choose>
                  <xsl:when test="valueCode = '' and valueValue = '' ">
                    <value xsi:type="CD" nullFlavor="UNK" />
                  </xsl:when>
                  <xsl:when test="valueCode != ''">
                    <value xsi:type="CD">
                      <xsl:attribute name="code">
                        <xsl:value-of select="valueCode"/>
                      </xsl:attribute>
                      <xsl:if test="valueCodeSystem != ''">
                        <xsl:attribute name="codeSystem">
                          <xsl:value-of select="valueCodeSystem"/>
                        </xsl:attribute>
                      </xsl:if>
                      <xsl:if test="boolean(valueCodeSystem) or (valueCodeSystem = '')">
                        <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                      </xsl:if>
                      <xsl:if test="valueInnerText != ''">
                        <originalText>
                          <xsl:value-of select="valueInnerText"/>
                        </originalText>
                      </xsl:if>
                    </value>
                  </xsl:when>
                  <xsl:when test="valueValue != ''">
                    <value xsi:type="PQ">
                      <xsl:attribute name="value">
                        <xsl:value-of select="valueValue"/>
                      </xsl:attribute>
                      <xsl:if test="boolean(valueUnit) and (valueUnit != '')">
                        <xsl:attribute name="unit">
                          <xsl:value-of select="valueUnit"/>
                        </xsl:attribute>
                      </xsl:if>
                    </value>
                  </xsl:when>
                </xsl:choose>
              </xsl:otherwise>
            </xsl:choose>-->

          </xsl:for-each>
          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasoncode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>
        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="Labrorders">
    <xsl:for-each select="/QRDA/labordersObjColl/Laborders">
      <entry>
        <observation classCode="OBS" moodCode="RQO">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Consolidation Plan of Care Activity Observation -->
          <templateId root="2.16.840.1.113883.10.20.22.4.44" extension="2014-06-09" />
          <!-- Lab Test Order -->
          <templateId root="2.16.840.1.113883.10.20.24.3.37" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>


          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="codeSystem" />
            <xsl:with-param name="code" select="code" />
            <xsl:with-param name="valueset" select="valueset" />
            <xsl:with-param name="sectiontype" select="'labtestorder'" />
            <xsl:with-param name="text" select="text" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>


          <!--<code xsi:type="CD">           
            <xsl:if test="code != ''">
              <xsl:attribute name="code">
                <xsl:value-of select="code"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="code = ''">
              <xsl:attribute name="nullFlavor">
                <xsl:text>NA</xsl:text>
              </xsl:attribute>
            </xsl:if>            
            
            <xsl:if test="CodeSystem != ''">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="CodeSystem"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="CodeSystem = '' or boolean(CodeSystem) = false">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.1</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="text"/>
            </originalText>
          </code>-->

          <text>
            <xsl:value-of select="text"/>
          </text>
          <statusCode code="completed" />
          <!-- Attribute: datetime -->
          <author>
            <time>
              <xsl:if test="time != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="time"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="time = ''">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </time>
            <assignedAuthor>
              <id nullFlavor="NA" root="52e1d0d0-2095-0132-1250-22000b411e27"/>
            </assignedAuthor>
          </author>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="rejectcode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <!--<xsl:if test="reasoncode != ''">
            <entryRelationship typeCode="RSON">
              <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
                 <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
                <statusCode code="completed"/>
                <effectiveTime>
                  <low>
                    <xsl:if test="time != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="time"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="time = ''">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </low>
                  <high>
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </high>
                </effectiveTime>
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="reasoncode"/>
                  </xsl:attribute>
                  <xsl:if test="rejectcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="rejectcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="rejectcodeSystem = '' or boolean(rejectcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </observation>
            </entryRelationship>
          </xsl:if>-->

        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="RiskCategoryAssessment">
    <xsl:for-each select="/QRDA/riskAssessmentListObj/riskAssessment">
      <entry>
        <observation classCode="OBS" moodCode="EVN">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Consolidation Assessment Scale Observation templateId -->
          <!--<templateId root="2.16.840.1.113883.10.20.22.4.69" />-->
          <!-- Risk Category Assessment -->
          <!--<templateId root="2.16.840.1.113883.10.20.24.3.69" extension="2016-02-01" />-->

          <templateId root="2.16.840.1.113883.10.20.24.3.144" extension="2016-08-01" />


          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>


          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="conceptCodeOID" />
            <xsl:with-param name="code" select="codeCode" />
            <xsl:with-param name="valueset" select="conceptValueOID" />
            <xsl:with-param name="sectiontype" select="'riskcategoryassessment'" />
            <xsl:with-param name="text" select="codeDisplayName" />
            <xsl:with-param name="negationFlag" select="negationInd" />

          </xsl:call-template>

          <!--<code codeSystem="2.16.840.1.113883.6.1">          
            <xsl:if test="code != ''">
              <xsl:attribute name="code">
                <xsl:value-of select="code"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="code = ''">
              <xsl:attribute name="nullFlavor">
                <xsl:text>NA</xsl:text>
              </xsl:attribute>
            </xsl:if>
          
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="text"/>
            </originalText>
          </code>-->

          <text>
            <xsl:value-of select="codeDisplayName"/>
          </text>
          <statusCode code="completed" />
          <effectiveTime>
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>



          <xsl:if test="valueCode != ''">
            <value xsi:type="CD">
              <xsl:if test="boolean(valueCodeValueSet) and (valueCodeValueSet != '')">
                <xsl:attribute name="sdtc:valueSet">
                  <xsl:value-of select="valueCodeValueSet"/>
                </xsl:attribute>
              </xsl:if>

              <xsl:attribute name="code">
                <xsl:value-of select="valueCode"/>
              </xsl:attribute>
              <xsl:if test="valueCodeSystem != ''">
                <xsl:attribute name="codeSystem">
                  <xsl:value-of select="valueCodeSystem"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="valueCodeSystem = ''">
                <xsl:attribute name="codeSystem">
                  <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="valueInnerText != ''">
                <originalText>
                  <xsl:value-of select="valueInnerText"/>
                </originalText>
              </xsl:if>
            </value>
          </xsl:if>

          <xsl:if test="valueValue != ''">
            <value xsi:type="PQ">
              <xsl:attribute name="value">
                <xsl:value-of select="valueValue"/>
              </xsl:attribute>
              <xsl:attribute name="unit">
                <xsl:value-of select="valueUnit"/>
              </xsl:attribute>
            </value>
          </xsl:if>

          <xsl:if test="valueCode = ''">
            <xsl:if test="valueInnerText != ''">
              <value xsi:type="ST">
                <xsl:value-of select="valueInnerText"/>
              </value>
            </xsl:if>
          </xsl:if>

          <xsl:if test="valueCode = '' and valueValue = '' and valueInnerText = ''">
            <value xsi:type="CD" nullFlavor="UNK" />
          </xsl:if>


          <!--<xsl:if test="boolean(resulttext) and (resulttext != '')">
            <xsl:choose>
              <xsl:when test="boolean(valuetype) and (valuetype = 'ST')">
                <value xsi:type="ST">
                  <xsl:value-of select="resulttext"/>
                </value>
              </xsl:when>
              <xsl:when test="boolean(unit) and (normalize-space(unit) = '')">
                <value xsi:type="ST">
                  <xsl:value-of select="resulttext"/>
                </value>
              </xsl:when>
              <xsl:when test="boolean(valuetype) =false or (valuetype = 'PQ')">
                <value xsi:type="PQ">
                  <xsl:attribute name="value">
                    <xsl:value-of select="resulttext"/>
                  </xsl:attribute>
                  <xsl:if test="boolean(unit) and (normalize-space(unit != ''))">
                    <xsl:attribute name="unit">
                      <xsl:value-of select="unit"/>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </xsl:when>
              <xsl:when test="boolean(valuetype) =false or (valuetype = 'CD')">
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="resultcode"/>
                  </xsl:attribute>
                  <xsl:if test="resultcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="resultcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="resultcodeSystem = ''  or boolean(resultcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="boolean(resultvalueSet)">
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="resultvalueSet"/>
                    </xsl:attribute>
                  </xsl:if>
                  <originalText>
                    <xsl:value-of select="resulttext"/>
                  </originalText>
                </value>

              </xsl:when>
            </xsl:choose>
          </xsl:if>
          <xsl:if test="resulttext = ''  or boolean(resulttext) = false">
            <value xsi:type="CD" nullFlavor="UNK"/>
          </xsl:if>-->

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="rejectcode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <!--<xsl:if test="reasoncode != ''">
            <entryRelationship typeCode="RSON">
              <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
                 <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
                <statusCode code="completed"/>
                <effectiveTime>
                  <low>
                    <xsl:if test="effectiveTimeLow != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="effectiveTimeLow"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </low>
                  <high>
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </high>
                </effectiveTime>
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="reasoncode"/>
                  </xsl:attribute>
                  <xsl:if test="rejectcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="rejectcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="rejectcodeSystem = '' or boolean(rejectcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </observation>
            </entryRelationship>
          </xsl:if>-->

        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="DiagnosticStudiesOrder">
    <xsl:for-each select="/QRDA/diagnosticStudiesOrderColl/DiagnosticStudiesOrder">
      <entry>
        <observation classCode="OBS" moodCode="RQO">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Consolidated Plan of Care Activity Observation 
       templateId (Implied Template) -->
          <templateId root="2.16.840.1.113883.10.20.22.4.44" extension="2014-06-09" />
          <!-- Diagnostic Study, Order template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.17" extension="2016-02-01" />

          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>

          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="codeSystem" />
            <xsl:with-param name="code" select="code" />
            <xsl:with-param name="valueset" select="valueSet" />
            <xsl:with-param name="sectiontype" select="'diagnosticstudies'" />
            <xsl:with-param name="text" select="text" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>

          <!--<code codeSystem="2.16.840.1.113883.6.1">

            <xsl:if test="code = ''">
              <xsl:attribute name="nullFlavor">
                <xsl:text>NA</xsl:text>
              </xsl:attribute>
            </xsl:if>
  
            <xsl:if test="code != ''">
              <xsl:attribute name="code">
                <xsl:value-of select="code"/>
              </xsl:attribute>
            </xsl:if>
            
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="text"/>
            </originalText>
          </code>-->
          <text>
            <xsl:value-of select="text"/>
          </text>
          <statusCode code="completed" />

          <!-- Attribute: datetime -->
          <author>
            <time>
              <xsl:if test="time != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="time"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="time = ''">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </time>
            <assignedAuthor>
              <id nullFlavor="NA" root="cee4f200-1fdc-0132-10dd-22000b411e27"/>
            </assignedAuthor>
          </author>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasoncode" />
            <xsl:with-param name="effectiveTimeLow" select="time" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="DiagnosticStudies">
    <xsl:for-each select="/QRDA/diagnosticStudiesColl/DiagnosticStudies">
      <entry>
        <observation classCode="OBS" moodCode="EVN">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Consolidated Procedure Activity Observation templateId (Implied Template) -->
          <templateId root="2.16.840.1.113883.10.20.22.4.13" extension="2014-06-09" />
          <!-- Diagnostic Study, Performed template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.18" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>


          <text>
            <xsl:value-of select="text"/>
          </text>
          <statusCode code="completed" />
          <effectiveTime>
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>

          <!--<value xsi:type="CD" nullFlavor="UNK"/>-->

          <xsl:if test="valueCode != ''">
            <value xsi:type="CD" sdtc:valueSet="2.16.840.1.113883.3.526.3.326">
              <xsl:attribute name="code">
                <xsl:value-of select="valueCode"/>
              </xsl:attribute>
              <xsl:if test="valueCodeSystem != ''">
                <xsl:attribute name="codeSystem">
                  <xsl:value-of select="valueCodeSystem"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="valueCodeSystem = ''">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:if>
              <xsl:if test="valueInnerText != ''">
                <originalText>
                  <xsl:value-of select="valueInnerText"/>
                </originalText>
              </xsl:if>
            </value>
          </xsl:if>

          <xsl:if test="valueValue != ''">
            <value xsi:type="PQ">
              <xsl:attribute name="value">
                <xsl:value-of select="valueValue"/>
              </xsl:attribute>
              <xsl:attribute name="unit">
                <xsl:value-of select="valueUnit"/>
              </xsl:attribute>
            </value>
          </xsl:if>

          <xsl:if test="valueCode = ''">
            <xsl:if test="valueInnerText != ''">
              <value xsi:type="ST">
                <xsl:value-of select="valueInnerText"/>
              </value>
            </xsl:if>
          </xsl:if>

          <xsl:if test="valueCode = '' and valueValue = '' and valueInnerText = ''">
            <value xsi:type="CD" nullFlavor="UNK" />
          </xsl:if>



        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="ProviderToProviderCommunication">
    <xsl:for-each select="/QRDA/providerToProviderCommunicationColl/ProviderToProviderCommunication">
      <entry>
        <act classCode="ACT" moodCode="EVN">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Communication from provider to provider -->
          <templateId root="2.16.840.1.113883.10.20.24.3.4" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>

          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="codeSystem" />
            <xsl:with-param name="code" select="code" />
            <xsl:with-param name="valueset" select="valueset" />
            <xsl:with-param name="sectiontype" select="'providertoprovider'" />
            <xsl:with-param name="text" select="text" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>

          <!--<code codeSystem="2.16.840.1.113883.6.96">
              <xsl:if test="code != ''">
                <xsl:attribute name="code">
                  <xsl:value-of select="code"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="code = ''">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>NA</xsl:text>
                </xsl:attribute>
              </xsl:if>
            
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="text"/>
            </originalText>
          </code>-->

          <text>
            <xsl:value-of select="text"/>
          </text>
          <statusCode code="completed" />
          <effectiveTime>
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <participant typeCode="AUT">
            <participantRole classCode="ASSIGNED">
              <code code="158965000" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" displayName="Medical Practitioner"/>
            </participantRole>
          </participant>
          <participant typeCode="IRCP">
            <participantRole classCode="ASSIGNED">
              <code code="158965000" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" displayName="Medical Practitioner"/>
            </participantRole>
          </participant>

          <xsl:if test="inFulfillmentOf1actReference != ''">
            <sdtc:inFulfillmentOf1 typeCode="FLFS">
              <sdtc:templateId root="2.16.840.1.113883.10.20.24.3.126" extension="2014-12-01"/>
              <sdtc:actReference classCode="ACT" moodCode="EVN">
                <sdtc:id root="1.3.6.1.4.1.115">
                  <xsl:attribute name="extension">
                    <xsl:value-of select="inFulfillmentOf1actReference"/>
                  </xsl:attribute>
                </sdtc:id>
              </sdtc:actReference>
            </sdtc:inFulfillmentOf1>
          </xsl:if>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasoncode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <!--<xsl:if test="reasoncode != ''">
            <entryRelationship typeCode="RSON">
              <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
                 <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
                <statusCode code="completed"/>
                <effectiveTime>
                  <low>
                    <xsl:if test="effectiveTimeLow != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="effectiveTimeLow"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </low>
                  <high>
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </high>
                </effectiveTime>
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="reasoncode"/>
                  </xsl:attribute>
                  <xsl:if test="rejectcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="rejectcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="rejectcodeSystem = '' or boolean(rejectcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </observation>
            </entryRelationship>
          </xsl:if>-->

        </act>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="ProviderToPatientCommunication">
    <xsl:for-each select="/QRDA/providerToPatientCommunicationColl/ProviderToPatientCommunication">
      <entry>
        <act classCode="ACT" moodCode="EVN">
          <!-- Communication from provider to provider -->
          <!--<xsl:if test="reasoncode != ''">
            <xsl:attribute name="negationInd">
              <xsl:text>true</xsl:text>
            </xsl:attribute>
          </xsl:if>-->

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <templateId root="2.16.840.1.113883.10.20.24.3.3"/>
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code codeSystem="2.16.840.1.113883.6.96">
            <xsl:attribute name="code">
              <xsl:value-of select="code"/>
            </xsl:attribute>
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="text"/>
            </originalText>
          </code>
          <text>
            <xsl:value-of select="text"/>
          </text>
          <statusCode code="completed"/>
          <effectiveTime>
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>

          <participant typeCode="AUT">
            <participantRole classCode="ASSIGNED">
              <code code="158965000" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" displayName="Medical Practitioner"/>
            </participantRole>
          </participant>

          <participant typeCode="IRCP">
            <participantRole classCode="PAT"/>
          </participant>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasoncode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <!--<xsl:if test="reasoncode != ''">
            <entryRelationship typeCode="RSON">
              <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
                 <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
                <statusCode code="completed"/>
                <effectiveTime>
                  <low>
                    <xsl:if test="effectiveTimeLow != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="effectiveTimeLow"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </low>
                  <high>
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </high>
                </effectiveTime>
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="reasoncode"/>
                  </xsl:attribute>
                  <xsl:if test="rejectcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="rejectcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="rejectcodeSystem = '' or boolean(rejectcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </observation>
            </entryRelationship>
          </xsl:if>-->
        </act>

      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="PatientToProviderCommunication">
    <xsl:for-each select="/QRDA/patientToProviderCommunicationColl/PatientToProviderCommunication">
      <entry>
        <act classCode="ACT" moodCode="EVN">
          <!-- Communication from provider to provider -->
          <!--<xsl:if test="reasoncode != ''">
            <xsl:attribute name="negationInd">
              <xsl:text>true</xsl:text>
            </xsl:attribute>
          </xsl:if>-->

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <templateId root="2.16.840.1.113883.10.20.24.3.2" extension="2016-02-01"/>
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code codeSystem="2.16.840.1.113883.6.96">
            <xsl:attribute name="code">
              <xsl:value-of select="code"/>
            </xsl:attribute>
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="text"/>
            </originalText>
          </code>
          <text>
            <xsl:value-of select="text"/>
          </text>
          <statusCode code="completed"/>
          <effectiveTime>
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <participant typeCode="AUT">
            <participantRole classCode="PAT">
              <code code="116154003" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" displayName="Patient"/>
            </participantRole>
          </participant>
          <participant typeCode="IRCP">
            <participantRole classCode="ASSIGNED">
              <code code="158965000" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" displayName="Medical Practitioner"/>
            </participantRole>
          </participant>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasoncode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <!--<xsl:if test="reasoncode != ''">
            <entryRelationship typeCode="RSON">
              <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
                 <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
                <statusCode code="completed"/>
                <effectiveTime>
                  <low>
                    <xsl:if test="effectiveTimeLow != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="effectiveTimeLow"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </low>
                  <high>
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </high>
                </effectiveTime>
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="reasoncode"/>
                  </xsl:attribute>
                  <xsl:if test="rejectcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="rejectcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="rejectcodeSystem = '' or boolean(rejectcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </observation>
            </entryRelationship>
          </xsl:if>-->

        </act>

      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="PatientCharacteristic">
    <xsl:for-each select="/QRDA/socialHistoryListObj/SocialHistory">
      <entry>
        <observation classCode="OBS" moodCode="EVN">
          <templateId root="2.16.840.1.113883.10.20.24.3.103" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code code="ASSERTION" displayName="Assertion" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>
          <statusCode code="completed" />
          <effectiveTime>
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <value codeSystem="2.16.840.1.113883.6.96" xsi:type="CD">
            <xsl:attribute name="code">
              <xsl:value-of select="conceptValue"/>
            </xsl:attribute>
            <xsl:if test="boolean(conceptValueOID) and (conceptValueOID != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="conceptValueOID"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="valueDisplayName"/>
            </originalText>
          </value>
        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>


  <xsl:template name="MedicationAdministered">
    <xsl:for-each select="/QRDA/immunizationListObj/Immunization">
      <entry>
        <act classCode="ACT" moodCode="EVN">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Medication, Administered template -->
          <!--<templateId root="2.16.840.1.113883.10.20.24.3.42"/>-->
          <templateId root="2.16.840.1.113883.10.20.24.3.140"/>
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>

          </id>
          <code code="416118004" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" displayName="Administration"/>
          <statusCode code="completed"/>
          <effectiveTime xsi:type="IVL_TS">
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <entryRelationship typeCode="COMP">
            <substanceAdministration classCode="SBADM" moodCode="EVN">
              <!-- Medication Activity (consolidation) template -->
              <templateId root="2.16.840.1.113883.10.20.22.4.52" extension="2014-06-09"/>
              <id>
                <xsl:attribute name="root">
                  <!--<xsl:value-of select="generate-id(id)"/>-->
                  <!--<xsl:text>cbde95d0-d9dd-0132-854b-22000b549a64</xsl:text>-->
                  <xsl:text>cbde95d0-</xsl:text>
                  <xsl:value-of select="id"/>
                </xsl:attribute>
              </id>
              <text>
                <xsl:value-of select="manufacturedMaterialObj/manufacturedMaterialTranslationDisplayName"/>
              </text>
              <statusCode code="completed" />
              <effectiveTime xsi:type="IVL_TS">
                <low>

                  <xsl:if test="effectiveTimeLow != ''">
                    <xsl:attribute name="value">
                      <xsl:value-of select="effectiveTimeLow"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </low>
                <high>
                  <xsl:if test="effectiveTimeHigh != ''">
                    <xsl:attribute name="value">
                      <xsl:value-of select="effectiveTimeHigh"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </high>
              </effectiveTime>

              <xsl:choose>
                <xsl:when test ="doseQuantity != ''">
                  <doseQuantity>
                    <xsl:attribute name="value">
                      <xsl:value-of select="doseQuantity"></xsl:value-of>
                    </xsl:attribute>
                    <xsl:attribute name="unit">
                      <xsl:value-of select="doseUnit"></xsl:value-of>
                    </xsl:attribute>
                  </doseQuantity>
                </xsl:when>
                <xsl:otherwise>
                  <doseQuantity nullFlavor="NA" />
                </xsl:otherwise>
              </xsl:choose>

              <consumable>
                <manufacturedProduct classCode="MANU">
                  <!-- Medication Information (consolidation) template -->
                  <templateId root="2.16.840.1.113883.10.20.22.4.54" extension="2014-06-09"/>
                  <id>
                    <xsl:attribute name="root">
                      <!--<xsl:value-of select="generate-id(id)"/>-->
                      <xsl:text>ckde95d0-</xsl:text>
                      <xsl:value-of select="id"/>
                    </xsl:attribute>
                  </id>
                  <manufacturedMaterial>

                    <xsl:call-template name="AddCodeNode">
                      <xsl:with-param name="codesystem" select="manufacturedMaterialObj/conceptCodeOID" />
                      <xsl:with-param name="code" select="manufacturedMaterialObj/conceptValue" />
                      <xsl:with-param name="valueset" select="manufacturedMaterialObj/conceptValueOID" />
                      <xsl:with-param name="sectiontype" select="'medadministered'" />
                      <xsl:with-param name="text" select="manufacturedMaterialObj/manufacturedMaterialDisplayName" />
                      <xsl:with-param name="negationFlag" select="negationInd" />
                    </xsl:call-template>

                    <!--<code>
                      <xsl:attribute name="sdtc:valueSet">
                        <xsl:value-of select="valueSet"/>
                      </xsl:attribute>
                      <xsl:if test="codeSystem != ''">
                        <xsl:attribute name="codeSystem">
                          <xsl:value-of select="codeSystem"/>
                        </xsl:attribute>
                      </xsl:if>
                      <xsl:if test="codeSystem = '' or boolean(codeSystem) = false">
                        <xsl:attribute name="codeSystem">
                          <xsl:text>2.16.840.1.113883.12.292</xsl:text>
                        </xsl:attribute>
                      </xsl:if>
                      <xsl:attribute name="code">
                        <xsl:value-of select="code"/>
                      </xsl:attribute>
                      <xsl:if test="boolean(valueSet) and (valueSet != '')">
                        <xsl:attribute name="sdtc:valueSet">
                          <xsl:value-of select="valueSet"/>
                        </xsl:attribute>
                      </xsl:if>
                      <originalText>
                        <xsl:value-of select="text"/>
                      </originalText>
                    </code>-->

                  </manufacturedMaterial>
                </manufacturedProduct>
              </consumable>
            </substanceAdministration>
          </entryRelationship>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="rejectionReasonCode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectionReason" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <!--<xsl:if test="reasoncode != ''">
            <entryRelationship typeCode="RSON">
              <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
                <id extension="EAA6B71BF5D85BC3CCE06E20A00F7212" />
                 <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
                <statusCode code="completed"/>
                <effectiveTime>
                  <low>
                    <xsl:if test="effectiveTimeLow != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="effectiveTimeLow"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </low>
                  <high>
                    <xsl:if test="effectiveTimeHigh != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="effectiveTimeHigh"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </high>
                </effectiveTime>
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="reasoncode"/>
                  </xsl:attribute>
                  <xsl:if test="rejectcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="rejectcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="rejectcodeSystem = '' or boolean(rejectcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>

                </value>
              </observation>
            </entryRelationship>
          </xsl:if>-->

        </act>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="MedicationOrder">
    <xsl:for-each select="/QRDA/medicationOrderListObj/Medication">
      <entry>
        <!--Medication Order -->
        <substanceAdministration classCode="SBADM" moodCode="RQO">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <templateId root="2.16.840.1.113883.10.20.22.4.42" extension="2014-06-09" />
          <!-- Medication, Order template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.47" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>

          </id>
          <text>
            <xsl:value-of select="manufacturedMaterialObj/manufacturedMaterialDisplayName"/>
          </text>
          <statusCode code="active" />
          <effectiveTime xsi:type="IVL_TS">
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <effectiveTime xsi:type="PIVL_TS" institutionSpecified="true" operator="A">
            <period unit="d">
              <xsl:if test="periodValue != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="periodValue"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="periodValue = ''">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>NA</xsl:text>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="periodUnit != ''">
                <xsl:attribute name="unit">
                  <xsl:value-of select="periodUnit"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="periodUnit = ''">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>NA</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </period>
          </effectiveTime>

          <xsl:choose>
            <xsl:when test ="doseQuantityValue != ''">
              <doseQuantity>
                <xsl:attribute name="value">
                  <xsl:value-of select="doseQuantityValue"></xsl:value-of>
                </xsl:attribute>
                <xsl:attribute name="unit">
                  <xsl:value-of select="doseQuantityUnit"></xsl:value-of>
                </xsl:attribute>
              </doseQuantity>
            </xsl:when>
            <xsl:otherwise>
              <doseQuantity nullFlavor="NA" />
            </xsl:otherwise>
          </xsl:choose>

          <consumable>
            <manufacturedProduct classCode="MANU">
              <!-- Medication Information (consolidation) template -->
              <templateId root="2.16.840.1.113883.10.20.22.4.23" extension="2014-06-09"/>
              <id>
                <xsl:attribute name="root">
                  <!--<xsl:value-of select="generate-id(id)"/>-->
                  <xsl:text>cbde95d0-d9dd-0132-854b-22000b549a64</xsl:text>
                </xsl:attribute>
              </id>
              <manufacturedMaterial>
                <xsl:call-template name="AddCodeNode">
                  <xsl:with-param name="codesystem" select="manufacturedMaterialObj/conceptCodeOID" />
                  <xsl:with-param name="code" select="manufacturedMaterialObj/conceptValue" />
                  <xsl:with-param name="valueset" select="manufacturedMaterialObj/conceptValueOID" />
                  <xsl:with-param name="sectiontype" select="'medication'" />
                  <xsl:with-param name="text" select="manufacturedMaterialObj/manufacturedMaterialDisplayName" />
                  <xsl:with-param name="negationFlag" select="negationInd" />
                </xsl:call-template>
              </manufacturedMaterial>
            </manufacturedProduct>
          </consumable>

          <author>
            <templateId root="2.16.840.1.113883.10.20.22.4.119" />
            <time>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </time>
            <assignedAuthor>
              <id root="4be72b40-3eed-0135-62c5-0ac514e14162" />
            </assignedAuthor>
          </author>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="rejectionReasonCode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectionReasonCodeSystem" />
            <xsl:with-param name="reasontext" select="rejectionReason" />
            <xsl:with-param name="reasonValueSystem" select="rejectionReasonValueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>
        </substanceAdministration>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="MedicationDispensed">
    <xsl:for-each select="/QRDA/medicationDispensedListObj/Medication">
      <entry>
        <act classCode="ACT" moodCode="EVN">
          <!-- Medication Dispensed Act -->
          <templateId root="2.16.840.1.113883.10.20.24.3.139"/>
          <id root="31866200-210c-0135-62c5-0ac514e14162" />
          <code code="SPLY" codeSystem="2.16.840.1.113883.5.6" displayName="supply" codeSystemName="ActClass"/>
          <entryRelationship typeCode="SUBJ">
            <!--Medication dispensed -->
            <supply classCode="SPLY" moodCode="EVN">
              <!--  Medication Dispensed template -->
              <templateId root="2.16.840.1.113883.10.20.24.3.45" extension="2016-02-01"/>
              <!-- Medication Dispense template -->
              <templateId root="2.16.840.1.113883.10.20.22.4.18" extension="2014-06-09"/>
              <id root="1.3.6.1.4.1.115">
                <xsl:attribute name="extension">
                  <xsl:value-of select="id"/>
                </xsl:attribute>
              </id>
              <text>
                <xsl:value-of select="manufacturedMaterialObj/manufacturedMaterialDisplayName"/>
              </text>
              <statusCode code="completed" />
              <effectiveTime xsi:type="IVL_TS">
                <low>
                  <xsl:if test="effectiveTimeLow != ''">
                    <xsl:attribute name="value">
                      <xsl:value-of select="effectiveTimeLow"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </low>
                <high>
                  <xsl:if test="effectiveTimeHigh != ''">
                    <xsl:attribute name="value">
                      <xsl:value-of select="effectiveTimeHigh"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </high>
              </effectiveTime>
              <product>
                <manufacturedProduct classCode="MANU">
                  <!-- Medication Information (consolidation) template -->
                  <templateId root="2.16.840.1.113883.10.20.22.4.23" extension="2014-06-09"/>
                  <id>
                    <xsl:attribute name="root">
                      <!--<xsl:value-of select="generate-id(id)"/>-->
                      <xsl:text>cbde95d0-d9dd-0132-854b-22000b549a64</xsl:text>
                    </xsl:attribute>
                  </id>
                  <manufacturedMaterial>
                    <xsl:call-template name="AddCodeNode">
                      <xsl:with-param name="codesystem" select="manufacturedMaterialObj/conceptCodeOID" />
                      <xsl:with-param name="code" select="manufacturedMaterialObj/conceptValue" />
                      <xsl:with-param name="valueset" select="manufacturedMaterialObj/conceptValueOID" />
                      <xsl:with-param name="sectiontype" select="'medication'" />
                      <xsl:with-param name="text" select="manufacturedMaterialObj/manufacturedMaterialDisplayName" />
                      <xsl:with-param name="negationFlag" select="negationInd" />
                    </xsl:call-template>
                  </manufacturedMaterial>
                </manufacturedProduct>
              </product>
            </supply>
          </entryRelationship>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="rejectionReasonCode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectionReasonCodeSystem" />
            <xsl:with-param name="reasontext" select="rejectionReason" />
            <xsl:with-param name="reasonValueSystem" select="rejectionReasonValueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

        </act>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="MedicationActive">
    <xsl:for-each select="/QRDA/medicationListObj/Medication">
      <entry>
        <substanceAdministration classCode="SBADM" moodCode="EVN">
          <!-- Medication Activity (consolidation) template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.16" extension="2014-06-09" />
          <!-- Medication, Active template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.41" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <text>
            <xsl:value-of select="text"/>
          </text>
          <statusCode code="active" />
          <effectiveTime xsi:type="IVL_TS">
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <effectiveTime xsi:type="PIVL_TS" institutionSpecified="true" operator="A">
            <period unit="d">
              <xsl:if test="periodValue != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="periodValue"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="periodValue = ''">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>NA</xsl:text>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="periodUnit != ''">
                <xsl:attribute name="unit">
                  <xsl:value-of select="periodUnit"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="periodUnit = ''">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>NA</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </period>
          </effectiveTime>

          <xsl:choose>
            <xsl:when test ="doseQuantityValue != ''">
              <doseQuantity>
                <xsl:attribute name="value">
                  <xsl:value-of select="doseQuantityValue"></xsl:value-of>
                </xsl:attribute>
                <xsl:attribute name="unit">
                  <xsl:value-of select="doseQuantityUnit"></xsl:value-of>
                </xsl:attribute>
              </doseQuantity>
            </xsl:when>
            <xsl:otherwise>
              <doseQuantity nullFlavor="NA" />
            </xsl:otherwise>
          </xsl:choose>

          <consumable>
            <manufacturedProduct classCode="MANU">
              <!-- Medication Information (consolidation) template -->
              <templateId root="2.16.840.1.113883.10.20.22.4.23" extension="2014-06-09"/>
              <id>
                <xsl:attribute name="root">
                  <!--<xsl:value-of select="generate-id(id)"/>-->
                  <xsl:text>cbde95d0-d9dd-0132-854b-22000b549a64</xsl:text>
                </xsl:attribute>
              </id>
              <manufacturedMaterial>
                <xsl:call-template name="AddCodeNode">
                  <xsl:with-param name="codesystem" select="manufacturedMaterialObj/conceptCodeOID" />
                  <xsl:with-param name="code" select="manufacturedMaterialObj/conceptValue" />
                  <xsl:with-param name="valueset" select="manufacturedMaterialObj/conceptValueOID" />
                  <xsl:with-param name="sectiontype" select="'medication'" />
                  <xsl:with-param name="text" select="manufacturedMaterialObj/manufacturedMaterialDisplayName" />
                  <xsl:with-param name="negationFlag" select="negationInd" />
                </xsl:call-template>
              </manufacturedMaterial>
            </manufacturedProduct>
          </consumable>

          <xsl:for-each select="supply">
            <entryRelationship typeCode="REFR">
              <supply classCode="SPLY" moodCode="EVN">
                <!-- Medication Dispense template -->
                <templateId root="2.16.840.1.113883.10.20.22.4.18" extension="2014-06-09"/>
                <id root="1.3.6.1.4.1.115">
                  <xsl:attribute name="extension">
                    <xsl:value-of select="id"/>
                  </xsl:attribute>
                </id>
                <statusCode code="completed"/>
                <effectiveTime>
                  <xsl:attribute name="value">
                    <xsl:value-of select="effectiveTime"/>
                  </xsl:attribute>
                </effectiveTime>
                <repeatNumber>
                  <xsl:attribute name="value">
                    <xsl:value-of select="repeatNumber"/>
                  </xsl:attribute>
                </repeatNumber>
                <quantity>
                  <xsl:attribute name="value">
                    <xsl:value-of select="quantityValue"/>
                  </xsl:attribute>
                  <xsl:attribute name="unit">
                    <xsl:value-of select="quantityUnit"/>
                  </xsl:attribute>
                </quantity>
                <product>
                  <manufacturedProduct classCode="MANU">
                    <!-- Medication Information (consolidation) template -->
                    <templateId root="2.16.840.1.113883.10.20.22.4.23" extension="2014-06-09"/>
                    <id root="3197c0e0-210c-0135-62c5-0ac514e14162"/>
                    <manufacturedMaterial>
                      <code codeSystem="2.16.840.1.113883.6.88" sdtc:valueSet="2.16.840.1.113883.3.464.1003.196.12.1171">
                        <!--<originalText>Medication, Active: Adhd Medications</originalText>-->
                        <xsl:attribute name="code">
                          <xsl:value-of select="supplycode"/>
                        </xsl:attribute>
                      </code>
                    </manufacturedMaterial>
                  </manufacturedProduct>
                </product>
              </supply>
            </entryRelationship>
          </xsl:for-each>

        </substanceAdministration>
      </entry>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="PhysicalExamFinding">
    <xsl:for-each select="/QRDA/physicalExamListObj/Observation">
      <entry>
        <!-- Physical Exam Finding -->
        <observation classCode="OBS" moodCode="EVN">

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!--  Result observation template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.13" extension="2014-06-09" />
          <!-- Physical Exam, Performed template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.59" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>


          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="conceptCodeOID" />
            <xsl:with-param name="code" select="codeCode" />
            <xsl:with-param name="valueset" select="conceptValueOID" />
            <xsl:with-param name="sectiontype" select="'physicalexamfinding'" />
            <xsl:with-param name="text" select="codeDisplayName" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>



          <text>
            <xsl:value-of select="codeDisplayName"/>
          </text>
          <statusCode code="completed" />
          <effectiveTime>
            <low>
              <xsl:if test="effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="effectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="effectiveTimeHigh = '' or boolean(effectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>
          <!--<xsl:if test="boolean(value) and (value != '')">
            <value xsi:type="PQ">
              <xsl:attribute name="value">
                <xsl:value-of select="value"/>
              </xsl:attribute>
              <xsl:if test="boolean(unit) and (unit != '')">
                <xsl:attribute name="unit">
                  <xsl:value-of select="unit"/>
                </xsl:attribute>
              </xsl:if>
            </value>
          </xsl:if>
          <xsl:if test="(boolean(value) = false) or (value = '')">
            <value xsi:type="PQ">
              <xsl:attribute name="nullFlavor">
                <xsl:text>UNK</xsl:text>
              </xsl:attribute>
            </value>
          </xsl:if>-->

          <xsl:if test="valueCode != ''">
            <value xsi:type="CD">
              <xsl:if test="boolean(valueCodeValueSet) and (valueCodeValueSet != '')">
                <xsl:attribute name="sdtc:valueSet">
                  <xsl:value-of select="valueCodeValueSet" />
                </xsl:attribute>
              </xsl:if>
              <xsl:attribute name="code">
                <xsl:value-of select="valueCode"/>
              </xsl:attribute>
              <xsl:if test="valueCodeSystem != ''">
                <xsl:attribute name="codeSystem">
                  <xsl:value-of select="valueCodeSystem"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="valueCodeSystem = ''">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:if>
              <xsl:if test="valueInnerText != ''">
                <originalText>
                  <xsl:value-of select="valueInnerText"/>
                </originalText>
              </xsl:if>
            </value>
          </xsl:if>

          <xsl:if test="valueValue != ''">
            <value xsi:type="PQ">
              <xsl:attribute name="value">
                <xsl:value-of select="valueValue"/>
              </xsl:attribute>
              <xsl:attribute name="unit">
                <xsl:value-of select="valueUnit"/>
              </xsl:attribute>
            </value>
          </xsl:if>

          <xsl:if test="valueCode = ''">
            <xsl:if test="valueInnerText != ''">
              <value xsi:type="ST">
                <xsl:value-of select="valueInnerText"/>
              </value>
            </xsl:if>
          </xsl:if>

          <xsl:if test="valueCode = '' and valueValue = '' and valueInnerText = ''">
            <value xsi:type="CD" nullFlavor="UNK" />
          </xsl:if>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasoncode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <!--<xsl:if test="reasoncode != ''">
            <entryRelationship typeCode="RSON">
              <observation classCode="OBS" moodCode="EVN">
                <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
                 <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
                <statusCode code="completed"/>
                <effectiveTime>
                  <low>
                    <xsl:if test="effectiveTimeLow != ''">
                      <xsl:attribute name="value">
                        <xsl:value-of select="effectiveTimeLow"/>
                      </xsl:attribute>
                    </xsl:if>
                    <xsl:if test="effectiveTimeLow = '' or boolean(effectiveTimeLow) = false">
                      <xsl:attribute name="nullFlavor">
                        <xsl:text>UNK</xsl:text>
                      </xsl:attribute>
                    </xsl:if>
                  </low>
                  <high>
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </high>
                </effectiveTime>
                <value xsi:type="CD">
                  <xsl:attribute name="code">
                    <xsl:value-of select="reasoncode"/>
                  </xsl:attribute>
                  <xsl:if test="rejectcodeSystem != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="rejectcodeSystem"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="rejectcodeSystem = '' or boolean(rejectcodeSystem) = false">
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </value>
              </observation>
            </entryRelationship>
          </xsl:if>-->

        </observation>
      </entry>
    </xsl:for-each>

  </xsl:template>
  <xsl:template name="ReportingParameters">
    <xsl:for-each select="/QRDA/reportingParametersObj">
      <component>
        <section>
          <!-- This is the templateId for Reporting Parameters section -->
          <templateId root="2.16.840.1.113883.10.20.17.2.1"/>
          <templateId extension="2016-03-01" root="2.16.840.1.113883.10.20.17.2.1.1"/>
          <code code="55187-9" codeSystem="2.16.840.1.113883.6.1"/>
          <title>Reporting Parameters</title>
          <text>
            <list>
              <item>
                <xsl:value-of select="title"/>
              </item>
            </list>
          </text>
          <entry typeCode="DRIV">
            <act classCode="ACT" moodCode="EVN">
              <!-- This is the templateId for Reporting Parameteres Act -->
              <templateId root="2.16.840.1.113883.10.20.17.3.8"/>
              <templateId extension="2016-03-01" root="2.16.840.1.113883.10.20.17.3.8.1"/>
              <id extension="296E5BF61A3BDA711B384B9C82A27BC9" />
              <code code="252116004" codeSystem="2.16.840.1.113883.6.96" displayName="Observation Parameters"/>
              <effectiveTime>
                <low>
                  <xsl:attribute name="value">
                    <xsl:value-of select="effectiveTimeLow"/>
                  </xsl:attribute>
                </low>
                <high>
                  <xsl:attribute name="value">
                    <xsl:value-of select="effectiveTimeHigh"/>
                  </xsl:attribute>
                </high>
              </effectiveTime>
            </act>
          </entry>
        </section>
      </component>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="MeasureSection">
    <component>
      <section>
        <!-- 
            *****************************************************************
            Measure Section
            *****************************************************************
          -->
        <!-- Measure Section -->
        <templateId root="2.16.840.1.113883.10.20.24.2.2"/>
        <!-- QRDA Category Report Section (V5) -->
        <templateId root="2.16.840.1.113883.10.20.27.2.1" extension="2020-12-01"/>
        <!-- QRDA Category III Measure Section (V5) -->
        <templateId root="2.16.840.1.113883.10.20.27.2.3" extension="2022-05-01"/>

        <!-- This is the LOINC code for "Measure document". This stays the same for all measure section required by QRDA standard -->
        <code code="55186-1" codeSystem="2.16.840.1.113883.6.1" displayName="measure section"/>
        <title>Measure Section</title>
        <text>

        </text>
        <!-- 1..* Organizers, each containing a reference to an eMeasure -->
        <xsl:choose>
          <!--liquid-->
          <xsl:when test="/QRDA/CQMNumber = '69'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="9A031BB8-3D9B-11E1-8634-00237D5BF174"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!--CMS69:SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Body Mass Index (BMI) Screening and Follow-Up Plan</text>

                  </externalDocument>
                </reference>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>

              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '68'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id extension="9A032D9C-3D9B-11E1-8634-00237D5BF174" root="2.16.840.1.113883.4.738"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Percentage of visits for patients aged 18 years and older for which the eligible professional or eligible clinician attests to documenting a list of current medications using all immediate resources available on the date of the encounter. This list must include ALL known prescriptions, over-the-counters, herbals, and vitamin/mineral/dietary (nutritional) supplements AND must contain the medications&#39; name, dosage, frequency and route of administration.</text>

                  </externalDocument>
                </reference>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>

              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '165'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="c928082-7a14-d92c-017a67b6f9971ea8"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!--CMS165 SHOULD This is the title of the eMeasure -->
                    <text>Controlling High Blood Pressure</text>

                  </externalDocument>
                </reference>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>

              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '138'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="E35791DF-5B25-41BB-B260-673337BC44A8"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!--CMS138 SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Tobacco Use: Screening and Cessation Intervention</text>
                  </externalDocument>
                </reference>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>

                <!--IPOP 2 Population-->
                <xsl:call-template name="IPOP_TWO_Component"/>

                <!--DENOM 2 Population-->
                <xsl:call-template name="DENOM_TWO_Component"/>

                <!--NUMERATOR 2 Population-->
                <xsl:call-template name="NUMERATOR_TWO_Component"/>

                <!--IPOP 3 Population-->
                <xsl:call-template name="IPOP_THREE_Component"/>

                <!--DENOM 3 Population-->
                <xsl:call-template name="DENOM_THREE_Component"/>

                <!--NUMERATOR 3 Population-->
                <xsl:call-template name="NUMERATOR_THREE_Component"/>

              </organizer>

            </entry>
          </xsl:when>

          <!--liquid-->
          <xsl:when test="/QRDA/CQMNumber = '2'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="9A031E24-3D9B-11E1-8634-00237D5BF174"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Screening for Depression and Follow-Up Plan</text>

                  </externalDocument>
                </reference>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '117'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="B2802B7A-3580-4BE8-9458-921AEA62B78C"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Childhood Immunization Status</text>

                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '159'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id extension="2c928082-7fac-c041-017faee6377002a5" root="2.16.840.1.113883.4.738"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>The percentage of adolescent patients 12 to 17 years of age and adult patients 18 years of age or older with major depression or dysthymia who reached remission 12 months (+/- 60 days) after an index event.</text>

                  </externalDocument>
                </reference>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>

              </organizer>
            </entry>
          </xsl:when>

          <xsl:when test="/QRDA/CQMNumber = '161'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id extension="2c928082-7a14-d92c-017a5d428e9516ff" root="2.16.840.1.113883.4.738"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Percentage of all patient visits for those patients that turn 18 or older during the measurement period in which a new or recurrent diagnosis of major depressive disorder (MDD) was identified and a suicide risk assessment was completed during the visit.</text>

                  </externalDocument>
                </reference>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

              </organizer>
            </entry>
          </xsl:when>

          <xsl:when test="/QRDA/CQMNumber = '126'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="59E84144-6332-4369-AEBD-03A7899CA3DA"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Use of Appropriate Medications for Asthma</text>

                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '136'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="703CC49B-B653-4885-80E8-245A057F5AE9"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>ADHD: Follow-Up Care for Children Prescribed Attention-Deficit/Hyperactivity Disorder (ADHD) Medication</text>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '155'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="0B63F730-25D6-4248-B11F-8C09C66A04EB"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Weight Assessment and Counseling for Nutrition and Physical Activity for Children and Adolescents</text>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '156'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="a3837ff8-1abc-4ba9-800e-fd4e7953adbd"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Use of High-Risk Medications in the Elderly</text>
                  </externalDocument>
                </reference>

                <!--Performance Rate 1-->
                <component>
                  <observation classCode="OBS" moodCode="EVN">
                    <templateId root="2.16.840.1.113883.10.20.27.3.30" extension="2016-09-01"/>
                    <templateId root="2.16.840.1.113883.10.20.27.3.14" extension="2016-09-01"/>
                    <templateId root="2.16.840.1.113883.10.20.27.3.25" extension="2016-11-01"/>
                    <code code="72510-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Performance Rate"/>
                    <statusCode code="completed"/>
                    <value xsi:type="INT">
                      <xsl:attribute name="value">
                        <xsl:value-of select="/QRDA/measures/PFRATES/RATE_1"/>
                      </xsl:attribute>
                    </value>
                    <reference typeCode="REFR">
                      <externalObservation classCode="OBS" moodCode="EVN">
                        <id root="E384D9B0-6AD6-45BC-B562-A57E46FC1E90"/>
                        <code code="NUMER" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Numerator"/>
                      </externalObservation>
                    </reference>
                  </observation>
                </component>

                <!--Performance Rate 2-->
                <component>
                  <observation classCode="OBS" moodCode="EVN">
                    <templateId root="2.16.840.1.113883.10.20.27.3.30" extension="2016-09-01"/>
                    <templateId root="2.16.840.1.113883.10.20.27.3.14" extension="2016-09-01"/>
                    <templateId root="2.16.840.1.113883.10.20.27.3.25" extension="2016-11-01"/>
                    <code code="72510-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Performance Rate"/>
                    <statusCode code="completed"/>
                    <value xsi:type="INT">
                      <xsl:attribute name="value">
                        <xsl:value-of select="/QRDA/measures/PFRATES/RATE_2"/>
                      </xsl:attribute>
                    </value>
                    <reference typeCode="REFR">
                      <externalObservation classCode="OBS" moodCode="EVN">
                        <id root="5577FDAE-5153-4B75-9B85-59CEF09CFC82"/>
                        <code code="NUMER" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Numerator"/>
                      </externalObservation>
                    </reference>
                  </observation>
                </component>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>

                <!--IPOP 2 Population-->
                <xsl:call-template name="IPOP_TWO_Component"/>

                <!--DENOM 2 Population-->
                <xsl:call-template name="DENOM_TWO_Component"/>

                <!--NUMERATOR 2 Population-->
                <xsl:call-template name="NUMERATOR_TWO_Component"/>

              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '149'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>

                <!-- Measure Reference and Results (V4) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.1" extension="2020-12-01"/>
                <!-- Measure Reference and Results - CMS (V5) template ID -->
                <templateId root="2.16.840.1.113883.10.20.27.3.17" extension="2022-05-01"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="  7c443b9b-1ad1-4467-b527-defc445701ff"/>
                    <code code="57024-2" displayName="Health Quality Measure Document" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" />
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Dementia: Cognative Assessment</text>
                  </externalDocument>
                </reference>

                <!--Performance Rate 1-->
                <component>
                  <observation classCode="OBS" moodCode="EVN">
                    <templateId root="2.16.840.1.113883.10.20.27.3.30" extension="2016-09-01"/>
                    <templateId root="2.16.840.1.113883.10.20.27.3.14" extension="2016-09-01"/>
                    <templateId root="2.16.840.1.113883.10.20.27.3.25" extension="2016-11-01"/>
                    <code code="72510-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Performance Rate"/>
                    <statusCode code="completed"/>
                    <value xsi:type="INT">
                      <xsl:attribute name="value">
                        <xsl:value-of select="/QRDA/measures/PFRATES/RATE_1"/>
                      </xsl:attribute>
                    </value>
                    <reference typeCode="REFR">
                      <externalObservation classCode="OBS" moodCode="EVN">
                        <id root="E384D9B0-6AD6-45BC-B562-A57E46FC1E90"/>
                        <code code="NUMER" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Numerator"/>
                      </externalObservation>
                    </reference>
                  </observation>
                </component>

                <!--IPOP Population-->
                <xsl:call-template name="IPOP_Component"/>
                
                <!--DENOM Population-->
                <xsl:call-template name="DENOM_Component"/>

                <!--NUMERATOR Population-->
                <xsl:call-template name="NUMERATOR_Component"/>

                <!--DENEXCEP Population-->
                <xsl:call-template name="DENEXCEP_Component"/>
              </organizer>

            </entry>
          </xsl:when>
        </xsl:choose>
      </section>
    </component>
  </xsl:template>
  <xsl:template name="documentationOf">
    <documentationOf typeCode="DOC">
      <serviceEvent classCode="PCPR">
        <!-- care provision -->
        <effectiveTime>
          <low>
            <xsl:attribute name="value">
              <xsl:value-of select="/QRDA/reportingParametersObj/effectiveTimeLow"/>
            </xsl:attribute>
          </low>
          <high nullFlavor='UNK'/>
        </effectiveTime>
        <!-- You can include multiple performers, each with an NPI, TIN, CCN. -->
        <performer typeCode="PRF">
          <time>
            <low>
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/reportingParametersObj/effectiveTimeLow"/>
              </xsl:attribute>
            </low>
            <high nullFlavor='UNK'/>
          </time>
          <assignedEntity>
            <!-- This is the provider NPI -->
            <id root="2.16.840.1.113883.4.6">
              <xsl:attribute name="extension">
                <xsl:value-of select="/QRDA/authorObj/NPI"/>
              </xsl:attribute>
            </id>
            <representedOrganization>
              <!-- This is the organization TIN -->
              <id root="2.16.840.1.113883.4.2" extension="731550582" />
              <name>
                <given>
                  <xsl:value-of select="/QRDA/authorObj/givenName"/>
                </given>
                <family>
                  <xsl:value-of select="/QRDA/authorObj/familyName"/>
                </family>
              </name>
            </representedOrganization>
          </assignedEntity>
        </performer>
      </serviceEvent>
    </documentationOf>
  </xsl:template>
  <xsl:template name="legalAuthenticator">
    <xsl:for-each select="/QRDA/legalObj">
      <legalAuthenticator>
        <time>
          <xsl:attribute name="value">
            <xsl:value-of select="time"/>
          </xsl:attribute>
        </time>
        <signatureCode code="S"/>
        <assignedEntity>
          <id root="bc01a5d1-3a34-4286-82cc-43eb04c972a7"/>
          <addr>
            <streetAddressLine>
              <xsl:value-of select="//custodianObj/streetAddressLine"/>
            </streetAddressLine>
            <city>
              <xsl:value-of select="//custodianObj/city"/>
            </city>
            <state>
              <xsl:value-of select="//custodianObj/state"/>
            </state>
            <postalCode>
              <xsl:value-of select="//custodianObj/postalCode"/>
            </postalCode>
            <country>
              <xsl:value-of select="//custodianObj/country"/>
            </country>
          </addr>
          <telecom use="WP">
            <xsl:attribute name="value">
              <xsl:value-of select="//custodianObj/phone"/>
            </xsl:attribute>
          </telecom>
          <assignedPerson>
            <name>
              <given>
                <xsl:value-of select="/QRDA/authorObj/givenName"/>
              </given>
              <family>
                <xsl:value-of select="/QRDA/authorObj/familyName"/>
              </family>
            </name>
          </assignedPerson>
          <representedOrganization>
            <id root="2.16.840.1.113883.19.5"/>
            <name>
              <xsl:value-of select="//custodianObj/phone"/>
            </name>
          </representedOrganization>
        </assignedEntity>
      </legalAuthenticator>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="custodian">
    <xsl:for-each select="/QRDA/custodianObj">
      <custodian>
        <assignedCustodian>
          <representedCustodianOrganization>
            <id root="2.16.840.1.113883.19.5"/>
            <name>
              <xsl:value-of select="name"/>
            </name>
            <telecom use="WP">
              <xsl:attribute name="value">
                <xsl:value-of select="phone"/>
              </xsl:attribute>
            </telecom>
            <addr>
              <streetAddressLine>
                <xsl:value-of select="streetAddressLine"/>
              </streetAddressLine>
              <city>
                <xsl:value-of select="city"/>
              </city>
              <state>
                <xsl:value-of select="state"/>
              </state>
              <postalCode>
                <xsl:value-of select="postalCode"/>
              </postalCode>
              <country>
                <xsl:value-of select="country"/>
              </country>
            </addr>
          </representedCustodianOrganization>
        </assignedCustodian>
      </custodian>
    </xsl:for-each>
  </xsl:template>

  <xsl:template name="author">

    <xsl:for-each select="/QRDA/authorObj">
      <author>
        <time value="20240312" />
        <assignedAuthor>
          <id root="2.16.840.1.113883.4.6" assigningAuthorityName="NPI">
            <xsl:attribute name="extension">
              <xsl:value-of select="NPI"/>
            </xsl:attribute>
          </id>
          <assignedPerson>
          <name>
            <given>
              <xsl:value-of select="givenName"/>          
            </given>
            <family>
              <xsl:value-of select="familyName"/>          
            </family>
          </name>
          <providerid>
            <xsl:value-of select="providerid"/>
          </providerid>
        </assignedPerson>
      </assignedAuthor>

    </author>
  </xsl:for-each>

  </xsl:template>

  <xsl:template name="IPOP_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="IPOP" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--IPOP Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/IPOP/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP/Payer/Payer_Other" />
        </xsl:call-template>

        <!--IPOP Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/IPOP/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>

  <xsl:template name="IPOP_TWO_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="IPOP" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--IPOP_TWO Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/IPOP_TWO/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_TWO/Payer/Payer_Other" />
        </xsl:call-template>

        <!--IPOP_TWO Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/IPOP_TWO/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>


  <xsl:template name="IPOP_THREE_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="IPOP" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--IPOP_THREE Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/IPOP_THREE/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/IPOP_THREE/Payer/Payer_Other" />
        </xsl:call-template>

        <!--IPOP_THREE Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/IPOP_THREE/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>

  <xsl:template name="DENOM_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="DENOM" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--DENOM Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/DENOM/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM/Payer/Payer_Other" />
        </xsl:call-template>

        <!--DENOM Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/DENOM/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>

  <xsl:template name="NUMERATOR_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="NUMER" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--NUMERATOR Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/NUMERATOR/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR/Payer/Payer_Other" />
        </xsl:call-template>

        <!--NUMERATOR Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/NUMERATOR/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>

    <xsl:template name="DENOM_TWO_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="DENOM" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--DENOM_TWO Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/DENOM_TWO/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_TWO/Payer/Payer_Other" />
        </xsl:call-template>

        <!--DENOM_TWO Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/DENOM_TWO/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>

  <xsl:template name="NUMERATOR_TWO_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="NUMER" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--NUMERATOR_TWO Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/NUMERATOR_TWO/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_TWO/Payer/Payer_Other" />
        </xsl:call-template>

        <!--NUMERATOR_TWO Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/NUMERATOR_TWO/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>


    <xsl:template name="DENOM_THREE_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="DENOM" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--DENOM_THREE Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/DENOM_THREE/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENOM_THREE/Payer/Payer_Other" />
        </xsl:call-template>

        <!--DENOM_THREE Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/DENOM_THREE/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>

  <xsl:template name="NUMERATOR_THREE_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="NUMER" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--NUMERATOR_THREE Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/NUMERATOR_THREE/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/NUMERATOR_THREE/Payer/Payer_Other" />
        </xsl:call-template>

        <!--NUMERATOR_THREE Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/NUMERATOR_THREE/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>


  <xsl:template name="DENEXCEP_Component">
    <component>
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.5" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.16" extension="2019-05-01" />
        <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
        <statusCode code="completed"/>
        <value xsi:type="CD" code="DENEXCEP" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode"/>

        <!--DENEXCEP Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="/QRDA/measures/DENEXCEP/count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'M'" />
          <xsl:with-param name="displayName" select="'Male'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Gender/male" />
        </xsl:call-template>

        <xsl:call-template name="Gender_Supplemental_Data">
          <xsl:with-param name="valueCode" select="'F'" />
          <xsl:with-param name="displayName" select="'Female'" />
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Gender/female" />
        </xsl:call-template>

        <!-- Ethnicities -->

        <xsl:call-template name="Not_Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Ethnicity/Not_Hisp_Lati" />
        </xsl:call-template>

        <xsl:call-template name="Hisp_Lati">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Ethnicity/Hisp_Lati" />
        </xsl:call-template>

        <!-- Races -->

        <xsl:call-template name="BLK_AFR_AME">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Race/BLK_AFR_AME" />
        </xsl:call-template>

        <xsl:call-template name="WHITE">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Race/WHITE" />
        </xsl:call-template>

        <xsl:call-template name="Asian">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Race/Asian" />
        </xsl:call-template>

        <xsl:call-template name="Americ_Indi">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Race/Americ_Indi" />
        </xsl:call-template>

        <xsl:call-template name="Native_Hawaiian">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Race/Native_Hawaiian" />
        </xsl:call-template>

        <xsl:call-template name="Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Race/Other" />
        </xsl:call-template>


        <!-- Payers -->

        <xsl:call-template name="Medicaid">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Payer/Medicaid" />
        </xsl:call-template>

        <xsl:call-template name="Medicare">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Payer/Medicare" />
        </xsl:call-template>

        <xsl:call-template name="Private">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Payer/Private" />
        </xsl:call-template>

        <xsl:call-template name="Payer_Other">
          <xsl:with-param name="count" select="/QRDA/measures/DENEXCEP/Payer/Payer_Other" />
        </xsl:call-template>

        <!--DENEXCEP Population ID from eMeasure-->
        <reference typeCode="REFR">
          <externalObservation classCode="OBS" moodCode="EVN">
            <id >
              <xsl:attribute name="root">
                <xsl:value-of select="/QRDA/measures/DENEXCEP/pop_id"/>
              </xsl:attribute>
            </id>
          </externalObservation>
        </reference>

      </observation>
    </component>
  </xsl:template>

  <xsl:template name="Gender_Supplemental_Data">

    <xsl:param name="valueCode" />
    <xsl:param name="displayName" />
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.6" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.21" extension="2016-11-01"/>
        <id >
          <xsl:if test="$valueCode = 'M'">
            <xsl:attribute name="root">
              <xsl:text>D5E68475-5760-11E7-1256-09173F13E4C5</xsl:text>
            </xsl:attribute>
          </xsl:if>
          <xsl:if test="$valueCode = 'F'">
            <xsl:attribute name="root">
              <xsl:text>D5E68476-5760-11E7-1256-09173F13E4C5</xsl:text>
            </xsl:attribute>
          </xsl:if>
        </id>
        <code code="76689-9" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Sex assigned at birth"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" codeSystem="2.16.840.1.113883.5.1" codeSystemName="AdministrativeGenderCode" >
          
          <xsl:attribute name="code">
            <xsl:value-of select="$valueCode"/>
          </xsl:attribute>

          <xsl:attribute name="displayName">
            <xsl:value-of select="$displayName"/>
          </xsl:attribute>

        </value>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>

  </xsl:template>

  <!--Ethnicity Supplemental Data Element - Not Hispanic or Latino-->

  <xsl:template name="Not_Hisp_Lati">
    
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.7" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.22" extension="2016-11-01"/>
        <id root="D5E68477-5760-11E7-1256-09173F13E4C5"/>
        <code code="69490-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Ethnicity"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="2186-5" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="Not Hispanic or Latino"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>

  </xsl:template>

  <!--Ethnicity Supplemental Data Element - Hispanic or Latino-->
  <xsl:template name="Hisp_Lati">

    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.7" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.22" extension="2016-11-01"/>
        <id root="D5E68478-5760-11E7-1256-09173F13E4C5"/>
        <code code="69490-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Ethnicity"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="2135-2" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="Hispanic or Latino"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>

  <!--Race Supplemental Data Element - Black or African American-->
  <xsl:template name="BLK_AFR_AME">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.8" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.19" extension="2016-11-01"/>
        <id root="D5E68479-5760-11E7-1256-09173F13E4C5"/>
        <code code="72826-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Race"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="2054-5" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="Black or African American"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>

  <!--Race Supplemental Data Element - White-->

  <xsl:template name="WHITE">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.8" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.19" extension="2016-11-01"/>
        <id root="D5E6847A-5760-11E7-1256-09173F13E4C5"/>
        <code code="72826-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Race"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="2106-3" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="White"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>
                  
                  
  <!--Race Supplemental Data Element - Asian-->
  <xsl:template name="Asian">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.8" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.19" extension="2016-11-01"/>
        <id root="D5E6847B-5760-11E7-1256-09173F13E4C5"/>
        <code code="72826-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Race"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="2028-9" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="Asian"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>
                  
  <!--Race Supplemental Data Element - American Indian or Alaska Native-->
  <xsl:template name="Americ_Indi">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.8" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.19" extension="2016-11-01"/>
        <id root="D5E6847C-5760-11E7-1256-09173F13E4C5"/>
        <code code="72826-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Race"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="1002-5" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="American Indian or Alaska Native"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>
                  
  <!--Race Supplemental Data Element - Native Hawaiian or Other Pacific Islander-->
  <xsl:template name="Native_Hawaiian">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.8" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.19" extension="2016-11-01"/>
        <id root="D5E68448-5760-11E7-1256-09173F13E4C5"/>
        <code code="72826-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Race"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="2076-8" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="Native Hawaiian or Other Pacific Islander"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>


                  
  <!--Race Supplemental Data Element - Other Race-->

  <xsl:template name="Other">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.8" extension="2016-09-01"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.19" extension="2016-11-01"/>
        <id root="D5E68448-5760-11E7-1256-09173F13E4C5"/>
        <code code="72826-1" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Race"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" code="2131-1" codeSystem="2.16.840.1.113883.6.238" codeSystemName="Race &amp; Ethnicity - CDC" displayName="Other Race"/>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>
                  
  <!--Payer Supplemental Data Element - Medicare-->
  <xsl:template name="Medicare">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.9" extension="2016-02-01"/>
        <templateId root="2.16.840.1.113883.10.20.24.3.55"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.18" extension="2018-05-01"/>
        <id root="D5E6847D-5760-11E7-1256-09173F13E4C5"/>
        <code code="48768-6" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Payment Source"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" nullFlavor="OTH">
          <translation code="A" codeSystem="2.16.840.1.113883.3.249.12" codeSystemName="CMS Clinical Codes" displayName="Medicare"/>
        </value>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>

  <!--Payer Supplemental Data Element - Medicaid-->
  <xsl:template name="Medicaid">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.9" extension="2016-02-01"/>
        <templateId root="2.16.840.1.113883.10.20.24.3.55"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.18" extension="2018-05-01"/>
        <id root="D5E6847E-5760-11E7-1256-09173F13E4C5"/>
        <code code="48768-6" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Payment Source"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" nullFlavor="OTH">
          <translation code="B" codeSystem="2.16.840.1.113883.3.249.12" codeSystemName="CMS Clinical Codes" displayName="Medicaid"/>
        </value>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>

  <!--Payer Supplemental Data Element - Private Health Insurance-->
  <xsl:template name="Private">
    <xsl:param name="count" />

    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.9" extension="2016-02-01"/>
        <templateId root="2.16.840.1.113883.10.20.24.3.55"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.18" extension="2018-05-01"/>
        <id root="D5E6847F-5760-11E7-1256-09173F13E4C5"/>
        <code code="48768-6" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Payment Source"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" nullFlavor="OTH">
          <translation code="C" codeSystem="2.16.840.1.113883.3.249.12" codeSystemName="CMS Clinical Codes" displayName="Private Health Insurance"/>
        </value>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>

  <!--Payer Supplemental Data Element - Other-->
  <xsl:template name="Payer_Other">
    <xsl:param name="count" />
    
    <entryRelationship typeCode="COMP">
      <observation classCode="OBS" moodCode="EVN">
        <templateId root="2.16.840.1.113883.10.20.27.3.9" extension="2016-02-01"/>
        <templateId root="2.16.840.1.113883.10.20.24.3.55"/>
        <templateId root="2.16.840.1.113883.10.20.27.3.18" extension="2018-05-01"/>
        <id root="D5E68480-5760-11E7-1256-09173F13E4C5"/>
        <code code="48768-6" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Payment Source"/>
        <statusCode code="completed"/>
        <effectiveTime>
          <low value="20240101"/>
          <high value="20241231"/>
        </effectiveTime>
        <value xsi:type="CD" nullFlavor="OTH">
          <translation code="D" codeSystem="2.16.840.1.113883.3.249.12" codeSystemName="CMS Clinical Codes" displayName="Other"/>
        </value>
        <!-- Count-->
        <entryRelationship typeCode="SUBJ" inversionInd="true">
          <observation classCode="OBS" moodCode="EVN">
            <templateId root="2.16.840.1.113883.10.20.27.3.3"/>
            <templateId root="2.16.840.1.113883.10.20.27.3.24"/>
            <code code="MSRAGG" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="rate aggregation"/>
            <statusCode code="completed"/>
            <value xsi:type="INT">
              <xsl:attribute name="value">
                <xsl:value-of select="$count"/>
              </xsl:attribute>
            </value>
            <methodCode code="COUNT" codeSystem="2.16.840.1.113883.5.84" codeSystemName="ObservationMethod" displayName="Count"/>
          </observation>
        </entryRelationship>
      </observation>
    </entryRelationship>
  </xsl:template>

</xsl:stylesheet>
