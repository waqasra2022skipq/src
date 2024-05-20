<!-- Title: CDA XSL StyleSheet Original Filename: cda.xsl  Version: 3.0 Revision History: 08/12/08 Jingdong Li updated Revision History: 12/11/09 KH updated  Revision History:  03/30/10 Jingdong Li updated. Revision History:  08/25/10 Jingdong Li updated Revision History:  09/17/10 Jingdong Li updated Revision History:  01/05/11 Jingdong Li updated Specification: ANSI/HL7 CDAR2 The current version and documentation are available at http://www.lantanagroup.com/resources/tools/.  We welcome feedback and contributions to tools@lantanagroup.com The stylesheet is the cumulative work of several developers; the most significant prior milestones were the foundation work from HL7  Germany and Finland (Tyylitiedosto) and HL7 US (Calvin Beebe), and the presentation approach from Tony Schaller, medshare GmbH provided at IHIC 2009. 
-->
<!-- LICENSE INFORMATION Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at  http://www.apache.org/licenses/LICENSE-2.0 
-->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns:sdtc="urn:hl7-org:sdtc" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"  xmlns="urn:hl7-org:v3" xmlns:voc="urn:hl7-org:v3/voc" >
  <xsl:output method="xml" indent="yes" omit-xml-declaration="yes" version="4.01" encoding="ISO-8859-1" doctype-system="http://www.w3.org/TR/html4/strict.dtd" doctype-public="-//W3C//DTD HTML 4.01//EN"/>
  <!-- global variable title -->

  <!--<xsl:variable name="title"> <xsl:choose>  <xsl:when test="string-length(/ClinicalDocument/title)  &gt;= 1"> <xsl:value-of select="/ClinicalDocument/title"/>  </xsl:when>  <xsl:when test="/ClinicalDocument/code/@displayName"> <xsl:value-of select="/ClinicalDocument/code/@displayName"/>  </xsl:when>  <xsl:otherwise> <xsl:text>Clinical Document</xsl:text>  </xsl:otherwise> </xsl:choose>  </xsl:variable>-->

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
    <!-- US Realm Header Template Id -->
    <templateId root="2.16.840.1.113883.10.20.22.1.1" extension="2015-08-01"/>
    <!-- QRDA templateId -->
    <templateId root="2.16.840.1.113883.10.20.24.1.1" extension="2017-08-01"/>
    <!-- QDM-based QRDA templateId -->
    <templateId root="2.16.840.1.113883.10.20.24.1.2" extension="2017-08-01"/>
    <!-- CMS QRDA templateId -->
    <templateId root="2.16.840.1.113883.10.20.24.1.3" extension="2018-02-01"/>
    <!-- This is the globally unique identifier for this QRDA document -->
    <id root="5b010313-eff2-432c-9909-6193d8416fac"/>
    <!-- QRDA document type code -->
    <code code="55182-0" codeSystem="2.16.840.1.113883.6.1" codeSystemName="LOINC" displayName="Quality Measure Report"/>
    <title>QRDA Incidence Report</title>
    <!-- This is the document creation time -->
    <effectiveTime>
      <xsl:attribute name="value">
        <xsl:value-of select="documentGeneratedDatetime"></xsl:value-of>
      </xsl:attribute>
    </effectiveTime>
    <confidentialityCode code="N" codeSystem="2.16.840.1.113883.5.25"/>
    <languageCode code="eng"/>
    <!--<xsl:value-of select="$title"/> <xsl:call-template name="addCSS"/>  <xsl:value-of select="$title"/>-->
    <!-- START display top portion of clinical document -->
    <xsl:call-template name="patientRoleObj"/>
    <xsl:call-template name="author"/>
    <xsl:call-template name="custodian"/>
    <xsl:call-template name="legalAuthenticator"/>
    <xsl:call-template name="documentationOf"/>
    <!-- Hard coded for now-->
    <component>
      <structuredBody>
        <xsl:call-template name="MeasureSection"/>
        <xsl:call-template name="ReportingParameters"/>
        <xsl:call-template name="PatientData"/>
      </structuredBody>
    </component>
    <!--<xsl:call-template name="documentGeneral"/>
		  <xsl:call-template name="documentationOf"/> <xsl:call-template name="componentof"/> <xsl:call-template name="participant"/> <xsl:call-template name="dataEnterer"/> <xsl:call-template name="authenticator"/> <xsl:call-template name="informant"/> <xsl:call-template name="informationRecipient"/>
			-->
    <!-- END display top portion of clinical document -->
  </xsl:template>
  <xsl:template name="PatientData">
    <component>
      <section>
        <!-- This is the templateId for Patient Data section -->
        <templateId root="2.16.840.1.113883.10.20.17.2.4"/>
        <!-- This is the templateId for Patient Data QDM section -->
        <templateId extension="2017-08-01" root="2.16.840.1.113883.10.20.24.2.1"/>
        <templateId extension="2018-02-01" root="2.16.840.1.113883.10.20.24.2.1.1"/>
        <code code="55188-7" codeSystem="2.16.840.1.113883.6.1"/>
        <title>Patient Data</title>
        <text></text>
        <xsl:call-template name="Problems"/>
        <xsl:call-template name="PatientCharacteristic"/>
        <xsl:call-template name="Encounter"/>
        <xsl:call-template name="MedicationOrder"/>
        <xsl:call-template name="MedicationAdministered"/>
        <xsl:call-template name="MedicationDispensed"/>
        <xsl:call-template name="MedicationActive"/>
        <xsl:call-template name="Intervention"/>
        <xsl:call-template name="InterventionOrder"/>
        <xsl:call-template name="Procedure"/>
        <xsl:call-template name="ProviderToProviderCommunication"/>
        <xsl:call-template name="PatientToProviderCommunication"/>
        <xsl:call-template name="ProviderToPatientCommunication"/>
        <xsl:call-template name="DiagnosticStudies"/>
        <xsl:call-template name="DiagnosticStudiesOrder"/>
        <!--<xsl:call-template name="Labresults"/>-->
        <xsl:call-template name="Labrorders"/>
        <xsl:call-template name="labresultsPerformed"/>
        <xsl:call-template name="PhysicalExamFinding"/>
        <xsl:call-template name="RiskCategoryAssessment"/>
        <xsl:call-template name="Procedureresults"/>
        <xsl:call-template name="Functionalstatus"/>
        <xsl:call-template name="PatientCharacteristicPayer"/>

        <!--TODO: Data not present for below templates-->
        <xsl:call-template name="Diagnosticstudyresult"/>
        <!--TODO: Data not present for below templates-->

        <!--MedicationDischarge Section not present-->

        <xsl:call-template name="ImmunizationAllergy"/>
        <xsl:call-template name="ImmunizationIntolerance"/>
        <xsl:call-template name="procedureintolerance"/>

      </section>
    </component>
  </xsl:template>

  <xsl:template name="labresultsPerformed">
    <xsl:for-each select="/QRDA/resultListObj/Result">
      <entry>
        <observation classCode="OBS" moodCode="EVN" >
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
                <value xsi:type="PQ" >
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
                    <value xsi:type="PQ" >
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


          <!--<code xsi:type="CD" >           
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
        <observation classCode="OBS" moodCode="EVN" >

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

          <!--<code codeSystem="2.16.840.1.113883.6.1" >          
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
                <value xsi:type="ST" >
                  <xsl:value-of select="resulttext"/>
                </value>
              </xsl:when>
              <xsl:when test="boolean(unit) and (normalize-space(unit) = '')">
                <value xsi:type="ST" >
                  <xsl:value-of select="resulttext"/>
                </value>
              </xsl:when>
              <xsl:when test="boolean(valuetype) =false or (valuetype = 'PQ')">
                <value xsi:type="PQ" >
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
                <value xsi:type="CD" >
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
            <value  xsi:type="CD" nullFlavor="UNK"/>
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

          <!--<code codeSystem="2.16.840.1.113883.6.1" >

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
  <xsl:template name="DiagnosticStudies">
    <xsl:for-each select="/QRDA/diagnosticStudiesColl/DiagnosticStudies">
      <entry>
        <observation classCode="OBS" moodCode="EVN" >

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


          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="codeSystem" />
            <xsl:with-param name="code" select="code" />
            <xsl:with-param name="valueset" select="codevalueset" />
            <xsl:with-param name="sectiontype" select="'diagnosticstudies'" />
            <xsl:with-param name="text" select="text" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>

          <!--<code codeSystem="2.16.840.1.113883.6.1" >
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
  <xsl:template name="ProviderToProviderCommunication">
    <xsl:for-each select="/QRDA/providerToProviderCommunicationColl/ProviderToProviderCommunication">
      <entry>
        <act classCode="ACT" moodCode="EVN" >

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Communication from provider to provider -->
          <templateId root="2.16.840.1.113883.10.20.24.3.4" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115" >
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

          <!--<code codeSystem="2.16.840.1.113883.6.96" >
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
        <act classCode="ACT" moodCode="EVN" >
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
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code codeSystem="2.16.840.1.113883.6.96" >
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
        <act classCode="ACT" moodCode="EVN" >
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
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code codeSystem="2.16.840.1.113883.6.96" >
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
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code code="ASSERTION" 	  displayName="Assertion" 	  codeSystem="2.16.840.1.113883.5.4" 	  codeSystemName="ActCode"/>
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
          <value codeSystem="2.16.840.1.113883.6.96" xsi:type="CD" >
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
  <xsl:template name="PatientCharacteristicPayer">
    <xsl:for-each select="/QRDA/patientRoleObj">
      <entry>
        <!-- Patient Characteristic Payer -->
        <observation classCode="OBS" moodCode="EVN">
          <templateId root="2.16.840.1.113883.10.20.24.3.55"/>
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="mrn"/>
            </xsl:attribute>
          </id>
          <code code="48768-6" codeSystemName="LOINC" codeSystem="2.16.840.1.113883.6.1" displayName="Payment source"/>
          <statusCode code="completed"/>
          <effectiveTime>
            <low nullFlavor="UNK"/>
          </effectiveTime>
          <value codeSystem="2.16.840.1.113883.3.221.5" xsi:type="CD" sdtc:valueSet="2.16.840.1.114222.4.11.3591">
            <xsl:if test="boolean(insuranceProvider) and (insuranceProvider != '')">
              <xsl:attribute name="code">
                <xsl:value-of select="insuranceProvider"/>
              </xsl:attribute>
              <originalText>
                <xsl:value-of select="insuranceProvider"/>
              </originalText>
            </xsl:if>
            <xsl:if test="(boolean(insuranceProvider) = false) or (insuranceProvider = '')">
              <xsl:attribute name="code">
                <xsl:text>349</xsl:text>
              </xsl:attribute>
              <originalText>
                <xsl:text>other</xsl:text>
              </originalText>
            </xsl:if>
          </value>
        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="Intervention">
    <xsl:for-each select="/QRDA/interventionPerformedListObj/Intervention">
      <entry>
        <act classCode="ACT" moodCode="EVN" >
          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>
          <!-- Consolidation CDA: Procedure Activity Act template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.12" extension="2014-06-09" />
          <!-- Intervention Performed Template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.32" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="conceptCodeOID" />
            <xsl:with-param name="code" select="codeCode" />
            <xsl:with-param name="valueset" select="conceptValueOID" />
            <xsl:with-param name="sectiontype" select="'interventionorder'" />
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
              <id root="52e1d0d0-2095-0132-1250-22000b411e27"/>
            </assignedAuthor>
          </author>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="rejectReasonCode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

        </act>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="InterventionOrder">
    <xsl:for-each select="/QRDA/interventionOrderedListObj/Intervention">
      <entry>
        <act classCode="ACT" moodCode="RQO">
          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>
          <!-- Consolidation CDA: Procedure Activity Act template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.39" extension="2014-06-09" />
          <!-- Intervention Order template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.31" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>

          <xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="conceptCodeOID" />
            <xsl:with-param name="code" select="codeCode" />
            <xsl:with-param name="valueset" select="conceptValueOID" />
            <xsl:with-param name="sectiontype" select="'interventionorder'" />
            <xsl:with-param name="text" select="codeDisplayName" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>

          <!--<code codeSystem="2.16.840.1.113883.6.96" >
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

          <text>
            <xsl:value-of select="codeDisplayName"/>
          </text>
          <statusCode code="active" />
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
              <id root="52e1d0d0-2095-0132-1250-22000b411e27"/>
            </assignedAuthor>
          </author>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="rejectReasonCode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="id" />
          </xsl:call-template>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasonCode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="reasoncodeSystem" />
            <xsl:with-param name="reasontext" select="reasonDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="reasoncodevalueset" />
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
                  <xsl:if test="reasontext != ''">
                    <xsl:attribute name="displayName">
                      <xsl:value-of select="rejectDisplayName"/>
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
  <xsl:template name="Observation">
    <xsl:for-each select="/QRDA/observationObjColl/Observation">
      <entry>
        <observation classCode="OBS" moodCode="EVN" >
          <!-- Consolidation Assessment Scale Observation templateId -->
          <templateId root="2.16.840.1.113883.10.20.22.4.69"/>
          <!-- Risk Category Assessment -->
          <templateId root="2.16.840.1.113883.10.20.24.3.69"/>
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code  codeSystem="2.16.840.1.113883.6.1" >
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
          <statusCode code="completed" />
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
          <value  xsi:type="CD" nullFlavor="UNK"/>

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
  <xsl:template name="Procedureresults">
    <xsl:for-each select="/QRDA/ProcedureresultsObjColl/Procedureresults">
      <entry>
        <procedure classCode="PROC" moodCode="EVN">
          <!-- Consolidated Procedure Activity Procedure TemplateId 
         (Implied Template) -->
          <templateId root="2.16.840.1.113883.10.20.22.4.14"/>
          <!-- QRDA Procedure, Result TemplateId -->
          <templateId root="2.16.840.1.113883.10.20.24.3.66"/>
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>

          </id>
          <code>
            <xsl:if test="procedurecode != ''">
              <xsl:attribute name="code">
                <xsl:value-of select="procedurecode"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="procedurecode = ''">
              <xsl:attribute name="nullFlavor">
                <xsl:text>NA</xsl:text>
              </xsl:attribute>
            </xsl:if>

            <xsl:if test="procedurecodeSystem != ''">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="procedurecodeSystem"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="procedurecodeSystem = '' or boolean(procedurecodeSystem) = false">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="boolean(procedurevalueSet)">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="procedurevalueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="proceduretext"/>
            </originalText>
          </code>
          <text>
            <xsl:value-of select="proceduretext"/>
          </text>
          <statusCode code="completed" />

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

          <entryRelationship typeCode="REFR">
            <observation classCode="OBS" moodCode="EVN">
              <!-- Result Observation template (consolidation) -->
              <templateId root="2.16.840.1.113883.10.20.22.4.2"/>
              <!-- Result template -->
              <templateId root="2.16.840.1.113883.10.20.24.3.87"/>
              <id>
                <xsl:attribute name="root">
                  <!--<xsl:value-of select="generate-id(id)"/>-->
                  <xsl:text>cbde95d0-d9dd-0132-854b-22000b549a64</xsl:text>
                </xsl:attribute>
              </id>
              <code>
                <xsl:if test="procedurecode != ''">
                  <xsl:attribute name="code">
                    <xsl:value-of select="procedurecode"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="procedurecode = ''">
                  <xsl:attribute name="nullFlavor">
                    <xsl:text>NA</xsl:text>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="procedurecodeSystem != ''">
                  <xsl:attribute name="codeSystem">
                    <xsl:value-of select="procedurecodeSystem"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="procedurecodeSystem = '' or boolean(procedurecodeSystem) = false">
                  <xsl:attribute name="codeSystem">
                    <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="boolean(procedurevalueSet)">
                  <xsl:attribute name="sdtc:valueSet">
                    <xsl:value-of select="procedurevalueSet"/>
                  </xsl:attribute>
                </xsl:if>
                <originalText>
                  <xsl:value-of select="proceduretext"/>
                </originalText>
              </code>
              <statusCode code="completed" />
              <effectiveTime>
                <xsl:attribute name="value">
                  <xsl:value-of select="effectiveTimeLow"/>
                </xsl:attribute>
              </effectiveTime>
              <value xsi:type="CD" >
                <xsl:attribute name="code">
                  <xsl:value-of select="procedureresultcode"/>
                </xsl:attribute>
                <xsl:if test="procedureresultcodeSystem != ''">
                  <xsl:attribute name="codeSystem">
                    <xsl:value-of select="procedureresultcodeSystem"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="procedureresultcodeSystem = ''  or boolean(procedureresultcodeSystem) = false">
                  <xsl:attribute name="codeSystem">
                    <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="boolean(procedureresultvalueSet)">
                  <xsl:attribute name="sdtc:valueSet">
                    <xsl:value-of select="procedureresultvalueSet"/>
                  </xsl:attribute>
                </xsl:if>
                <originalText>
                  <xsl:value-of select="procedureresulttext"/>
                </originalText>
              </value>
            </observation>
          </entryRelationship>
        </procedure>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="Functionalstatus">
    <xsl:for-each select="/QRDA/FunctionalstatusObjColl/Functionalstatus">
      <entry>
        <observation classCode="OBS" moodCode="EVN">
          <!-- Functional Status Result Observation (consolidation) template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.67"/>
          <!-- Functional Status, Result template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.28"/>
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code codeSystem="2.16.840.1.113883.6.1" >
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

          <statusCode code="completed" />

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

          <!-- Result -->
          <value xsi:type="CD" nullFlavor="UNK"/>
        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="Diagnosticstudyresult">
    <xsl:for-each select="/QRDA/DiagnosticstudyresultObjColl/Diagnosticstudyresult">
      <entry>
        <observation classCode="OBS" moodCode="EVN" >
          <!-- Consolidated Result Observation templateId (Implied Template) -->
          <templateId root="2.16.840.1.113883.10.20.22.4.2"/>
          <!-- Diagnostic Study, Result template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.20"/>
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>

          </id>
          <code>
            <xsl:attribute name="code">
              <xsl:value-of select="DiagnosticstudyresultCode"/>
            </xsl:attribute>
            <xsl:if test="DiagnosticstudyresultCodeSystem != ''">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="DiagnosticstudyresultCodeSystem"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="DiagnosticstudyresultCodeSystem = '' or boolean(DiagnosticstudyresultCodeSystem) = false">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.1</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="boolean(DiagnosticstudyresultvalueSet)">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="DiagnosticstudyresultvalueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="Diagnosticstudyresulttext"/>
            </originalText>
          </code>
          <text>
            <xsl:value-of select="Diagnosticstudyresulttext"/>
          </text>
          <statusCode code="completed" />
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
          <value xsi:type="CD">
            <xsl:attribute name="code">
              <xsl:value-of select="valuecode"/>
            </xsl:attribute>
            <xsl:if test="valuecodeSystem != ''">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="valuecodeSystem"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="valuecodeSystem = '' or boolean(valuecodeSystem) = false">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.1</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="valuetext"/>
            </originalText>
          </value>
        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="Labresults">
    <xsl:for-each select="/QRDA/resultListObj/Result/resultObs/ResultObs">
      <entry>
        <!--Laboratory test, result -->
        <observation classCode="OBS" moodCode="EVN">
          <!--  Result Observation (consolidation) template  -->
          <templateId root="2.16.840.1.113883.10.20.22.4.2"/>
          <!-- Laboratory Test, Result template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.40"/>
          <!--<templateId root="2.16.840.1.113883.10.20.24.3.38"/>-->
          <templateId root="2.16.840.1.113883.10.20.24.3.38" extension="2016-02-01"/>
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>

          </id>
          <code  codeSystem="2.16.840.1.113883.6.1" >
            <xsl:attribute name="code">
              <xsl:value-of select="code"/>
            </xsl:attribute>
            <xsl:if test="boolean(valueSet) and (valueSet != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="valueSet"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="displayName"/>
            </originalText>
          </code>
          <text>
            <xsl:value-of select="displayName"/>
          </text>
          <statusCode code="completed" />
          <effectiveTime>
            <low>
              <xsl:attribute name="value">
                <xsl:value-of select="effectiveTime"/>
              </xsl:attribute>
            </low>
            <high>
              <xsl:attribute name="value">
                <xsl:value-of select="effectiveTime"/>
              </xsl:attribute>
            </high>
          </effectiveTime>
          <xsl:if test="boolean(valuetype) and (valuetype != '')">
            <xsl:if test="boolean(valuetype) and (valuetype = 'ST')">
              <value xsi:type="ST" >
                <xsl:value-of select="valueValue"/>
              </value>
            </xsl:if>
            <xsl:if test="boolean(valuetype) =false or (valuetype = 'PQ')">
              <value xsi:type="PQ" >
                <xsl:attribute name="value">
                  <xsl:value-of select="valueValue"/>
                </xsl:attribute>
                <xsl:if test="boolean(valueUnit) and (valueUnit != '')">
                  <xsl:attribute name="unit">
                    <xsl:value-of select="valueUnit"/>
                  </xsl:attribute>
                </xsl:if>
              </value>
            </xsl:if>
          </xsl:if>
          <xsl:if test="(boolean(value) = false) or (value = '')">
            <value xsi:type="PQ" >
              <xsl:attribute name="nullFlavor">
                <xsl:text>UNK</xsl:text>
              </xsl:attribute>
            </value>
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
  <xsl:template name="AddReasonNode" >
    <xsl:param name="reasoncode" />
    <xsl:param name="effectiveTimeLow" />
    <xsl:param name="reasoncodeSystem" />
    <xsl:param name="reasontext" />
    <xsl:param name="reasonValueSystem"/>
    <xsl:param name="reasonid"/>

    <xsl:if test="$reasoncode != ''">
      <entryRelationship typeCode="RSON">
        <observation classCode="OBS" moodCode="EVN">
          <templateId root="2.16.840.1.113883.10.20.24.3.88" extension="2014-12-01" />
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:text>A5FB1A9-</xsl:text>
              <xsl:value-of select="$reasonid"/>
            </xsl:attribute>
          </id>
          <code code="77301-0" codeSystem="2.16.840.1.113883.6.1" displayName="reason" codeSystemName="LOINC" />
          <statusCode code="completed"/>
          <effectiveTime>
            <low>
              <xsl:if test="$effectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="$effectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="$effectiveTimeLow = '' or boolean($effectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <!--<high>
              <xsl:attribute name="nullFlavor">
                <xsl:text>UNK</xsl:text>
              </xsl:attribute>
            </high>-->
          </effectiveTime>
          <value xsi:type="CD">
            <xsl:attribute name="code">
              <xsl:value-of select="$reasoncode"/>
            </xsl:attribute>
            <xsl:if test="$reasoncodeSystem != ''">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="$reasoncodeSystem"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="$reasoncodeSystem = '' or boolean($reasoncodeSystem) = false">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="$reasontext != ''">
              <xsl:attribute name="displayName">
                <xsl:value-of select="$reasontext"/>
              </xsl:attribute>
            </xsl:if>

            <xsl:if test="$reasonValueSystem != ''">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="$reasonValueSystem"/>
              </xsl:attribute>
            </xsl:if>
          </value>
        </observation>
      </entryRelationship>
    </xsl:if>

  </xsl:template>
  <xsl:template name="AddCodeValueBasedOnValueSet">
    <xsl:param name="codesystemForAddCode" />
    <xsl:param name="valuesetForAddCode" />
    <xsl:param name="sectiontypeForAddCode" />
  </xsl:template>
  <xsl:template name="AddCodeNode" >
    <xsl:param name="codesystem" />
    <xsl:param name="code" />
    <xsl:param name="valueset" />
    <xsl:param name="sectiontype" />
    <xsl:param name="text"/>
    <xsl:param name="negationFlag"/>
    <!--<p>
      -->
    <!--Title: <xsl:value-of select = "$title" />-->
    <!--
    </p>-->

    <code>
      <xsl:choose>
        <!--<xsl:when test="$code != '' and $code = '73832-8' and $sectiontype = 'riskcategoryassessment'">-->
        <xsl:when test="$code != '' and $negationFlag = 'true'">
          <xsl:attribute name="nullFlavor">
            <xsl:text>NA</xsl:text>
          </xsl:attribute>
        </xsl:when>

        <xsl:when test="$code != ''">
          <xsl:attribute name="code">
            <xsl:value-of select="$code" />
          </xsl:attribute>
        </xsl:when>

        <xsl:otherwise>
          <xsl:attribute name="nullFlavor">
            <xsl:text>NA</xsl:text>
          </xsl:attribute>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:choose>
        <xsl:when test="$codesystem != ''">
          <xsl:attribute name="codeSystem">
            <xsl:value-of select="$codesystem" />
          </xsl:attribute>
        </xsl:when>
        <xsl:otherwise>
          <xsl:choose>
            <xsl:when test="$sectiontype = 'procedure'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'providertoprovider'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'diagnosticstudies'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.1</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'interventionorder'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'physicalexamfinding'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.1</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'medication'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.88</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'riskcategoryassessment'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.1</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'labtestorder'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.1</xsl:text>
              </xsl:attribute>
            </xsl:when>
            <xsl:when test="$sectiontype = 'medadministered'">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.12.292</xsl:text>
              </xsl:attribute>
            </xsl:when>

          </xsl:choose>
        </xsl:otherwise>
      </xsl:choose>

      <xsl:if test="$valueset != ''">
        <xsl:attribute name="sdtc:valueSet">
          <xsl:value-of select="$valueset" />
        </xsl:attribute>
      </xsl:if>


      <originalText>
        <xsl:value-of select="$text"/>
      </originalText>
    </code>
  </xsl:template>
  <xsl:template name="ImmunizationIntolerance">
    <xsl:for-each select="/QRDA/ImmunizationIntoleranceObjColl/ImmunizationIntolerance">
      <entry>
        <observation classCode="OBS" moodCode="EVN">
          <!-- consolidation CDA Allergy Observation template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>
          <templateId root="2.16.840.1.113883.10.20.24.3.46" extension="2016-02-01"/>
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code code="ASSERTION"
                displayName="Assertion"
                codeSystem="2.16.840.1.113883.5.4"
                codeSystemName="ActCode"/>
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
          <value xsi:type="CD"
                  code="59037007"
                  displayName="Drug intolerance"
                  codeSystem="2.16.840.1.113883.6.96"
                  codeSystemName="SNOMED CT"/>

          <participant typeCode="CSM">
            <participantRole classCode="MANU">
              <playingEntity classCode="MMAT">
                <code>
                  <xsl:attribute name="code">
                    <xsl:value-of select="code"/>
                  </xsl:attribute>
                  <xsl:attribute name="codeSystem">
                    <xsl:value-of select="codeSystem"/>
                  </xsl:attribute>
                  <xsl:if test="boolean(valueSet) and (valueSet != '')">
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="valueSet"/>
                    </xsl:attribute>
                  </xsl:if>
                  <originalText>
                    <xsl:value-of select="name"/>
                  </originalText>
                </code>
                <name>
                  <xsl:value-of select="name"/>
                </name>
              </playingEntity>
            </participantRole>
          </participant>
        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="ImmunizationAllergy">
    <xsl:for-each select="/QRDA/ImmunizationAllergyObjColl/ImmunizationAllergy">
      <entry>
        <observation classCode="OBS" moodCode="EVN">
          <!-- consolidation CDA Allergy observation template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.7" extension="2014-06-09"/>
          <!--  Medication Allergy -->
          <templateId root="2.16.840.1.113883.10.20.24.3.44" extension="2016-02-01"/>
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
          <value code="416098002" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED CT" displayName="Drug allergy" xsi:type="CD"/>
          <participant typeCode="CSM">
            <participantRole classCode="MANU">
              <playingEntity classCode="MMAT">
                <code>
                  <xsl:attribute name="code">
                    <xsl:value-of select="code"/>
                  </xsl:attribute>
                  <xsl:attribute name="codeSystem">
                    <xsl:value-of select="codeSystem"/>
                  </xsl:attribute>
                  <xsl:if test="boolean(valueSet) and (valueSet != '')">
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="valueSet"/>
                    </xsl:attribute>
                  </xsl:if>
                  <originalText>
                    <xsl:value-of select="name"/>
                  </originalText>
                </code>
                <name>
                  <xsl:value-of select="name"/>
                </name>
              </playingEntity>
            </participantRole>
          </participant>
        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="procedureintolerance">
    <xsl:for-each select="/QRDA/ProcedureIntoleranceObjColl/ProcedureIntolerance">
      <entry>
        <observation classCode="OBS" moodCode="EVN">
          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>
          <templateId root="2.16.840.1.113883.10.20.24.3.62" extension="2016-02-01"/>
          <templateId root="2.16.840.1.113883.10.20.24.3.104" extension="2016-02-01"/>
          <id root="1.3.6.1.4.1.115">
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>
          <code code="ASSERTION" codeSystem="2.16.840.1.113883.5.4" codeSystemName="ActCode" displayName="Assertion"/>
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
          <value xsi:type="CD">
            <xsl:attribute name="code">
              <xsl:value-of select="procedurevalue"/>
            </xsl:attribute>
            <xsl:attribute name="codeSystem">
              <xsl:value-of select="procedurevaluecodeSystem"/>
            </xsl:attribute>
            <xsl:attribute name="displayName">
              <xsl:value-of select="procedurevaluedisplay"/>
            </xsl:attribute>
          </value>

          <xsl:choose>
            <xsl:when test="procedureperfcode != ''">

              <entryRelationship typeCode="CAUS">
                <xsl:if test="procedureperfcodeInversionInd != '' and procedureperfcodeInversionInd = 'true'">
                  <xsl:attribute name="inversionInd">
                    <xsl:value-of select="procedureperfcodeInversionInd"/>
                  </xsl:attribute>
                </xsl:if>
                <procedure classCode="PROC" moodCode="EVN">
                  <!--  Procedure performed template -->
                  <templateId root="2.16.840.1.113883.10.20.24.3.64" extension="2016-02-01"/>
                  <!-- Procedure Activity Procedure-->
                  <templateId root="2.16.840.1.113883.10.20.22.4.14" extension="2014-06-09"/>
                  <id root="1.3.6.1.4.1.115">
                    <xsl:attribute name="extension">
                      <xsl:value-of select="procedureperfcodeid"/>
                    </xsl:attribute>
                  </id>

                  <code>
                    <xsl:attribute name="code">
                      <xsl:value-of select="procedureperfcode"/>
                    </xsl:attribute>
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="procedureperfcodesystem"/>
                    </xsl:attribute>
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="procedureperfvalueset"/>
                    </xsl:attribute>

                    <originalText>
                      <xsl:value-of select="procedureperftext"/>
                    </originalText>
                  </code>
                  <text>
                    <xsl:value-of select="procedureperftext"/>
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
                    </high>
                  </effectiveTime>
                </procedure>
              </entryRelationship>
            </xsl:when>
            <xsl:otherwise>
            </xsl:otherwise>
          </xsl:choose>

          <xsl:call-template name="AddReasonNode">
            <xsl:with-param name="reasoncode" select="reasoncode" />
            <xsl:with-param name="effectiveTimeLow" select="effectiveTimeLow" />
            <xsl:with-param name="reasoncodeSystem" select="rejectcodeSystem" />
            <xsl:with-param name="reasontext" select="rejectDisplayName" />
            <xsl:with-param name="reasonValueSystem" select="rejectcodevalueset" />
            <xsl:with-param name="reasonid" select="procedureperfcodeid" />
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

        </observation>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="Procedure">
    <xsl:for-each select="/QRDA/procedureListObj/Procedure">
      <entry>
        <procedure classCode="PROC" moodCode="EVN" >

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!--  Procedure performed template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.64" extension="2016-02-01" />
          <!-- Procedure Activity Procedure-->
          <templateId root="2.16.840.1.113883.10.20.22.4.14" extension="2014-06-09" />
          <id root="1.3.6.1.4.1.115" >
            <xsl:attribute name="extension">
              <xsl:value-of select="id"/>
            </xsl:attribute>
          </id>

          <!--<xsl:call-template name="AddCodeNode">
            <xsl:with-param name="codesystem" select="conceptCodeOID" />
            <xsl:with-param name="code" select="codeCode" />
            <xsl:with-param name="valueset" select="conceptValueOID" />
            <xsl:with-param name="sectiontype" select="'procedure'" />
            <xsl:with-param name="text" select="codeDisplayName" />
            <xsl:with-param name="negationFlag" select="negationInd" />
          </xsl:call-template>-->
          <code>
            <xsl:if test="codeCode != ''">
              <xsl:attribute name="code">
                <xsl:value-of select="codeCode"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="codeCode = ''">
              <xsl:attribute name="nullFlavor">
                <xsl:text>NA</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="conceptCodeOID != ''">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="conceptCodeOID"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="conceptCodeOID = ''">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="boolean(conceptValueOID) and (conceptValueOID != '')">
              <xsl:attribute name="sdtc:valueSet">
                <xsl:value-of select="conceptValueOID"/>
              </xsl:attribute>
            </xsl:if>
            <originalText>
              <xsl:value-of select="procedure"/>
            </originalText>
          </code>
          <!--<code>
    			  <xsl:if test="procedurecode != ''">
              <xsl:attribute name="code">
                <xsl:value-of select="procedurecode"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="procedurecode = ''">
              <xsl:attribute name="nullFlavor">
                <xsl:text>NA</xsl:text>
              </xsl:attribute>
            </xsl:if>               
            <xsl:if test="procedurecodeSystem != ''">
              <xsl:attribute name="codeSystem">
                <xsl:value-of select="procedurecodeSystem"/>
              </xsl:attribute>
            </xsl:if>
            <xsl:if test="procedurecodeSystem = ''">
              <xsl:attribute name="codeSystem">
                <xsl:text>2.16.840.1.113883.6.96</xsl:text>
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

          <xsl:choose>
            <xsl:when test="procedureresultvalue != ''">
              <entryRelationship typeCode="REFR">
                <observation classCode="OBS" moodCode="EVN">
                  <!-- Conforms to C-CDA R2 Result Observation (V2) -->
                  <templateId root="2.16.840.1.113883.10.20.22.4.2" extension="2015-08-01"/>
                  <!-- Result (QRDA I R3) -->
                  <templateId root="2.16.840.1.113883.10.20.24.3.87" extension="2016-02-01"/>
                  <id root="1.3.6.1.4.1.115" >
                    <xsl:attribute name="extension">
                      <xsl:value-of select="id"/>
                    </xsl:attribute>
                  </id>
                  <code>
                    <xsl:attribute name="code">
                      <xsl:value-of select="codeCode"/>
                    </xsl:attribute>
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="procedurecodeSystem"/>
                    </xsl:attribute>
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="conceptValueOID"/>
                    </xsl:attribute>
                  </code>
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
                      <xsl:value-of select="procedureresultvalue"/>
                    </xsl:attribute>
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="procedureresultvaluecodeSystem"/>
                    </xsl:attribute>
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="procedureresultvalueValueSet"/>
                    </xsl:attribute>
                    <originalText>
                      <xsl:value-of select="procedureresultvaluetext"/>
                    </originalText>
                  </value>
                </observation>
              </entryRelationship>
            </xsl:when>
            <xsl:otherwise>
            </xsl:otherwise>
          </xsl:choose>

        </procedure>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="Problems">
    <xsl:for-each select="/QRDA/problemListObj/Problem">
      <entry>
        <act classCode="ACT" moodCode="EVN">
          <!--  Problem observation template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.3" extension="2015-08-01" />
          <!-- Diagnosis Concern Act -->
          <templateId root="2.16.840.1.113883.10.20.24.3.137" />
          <id root="2af14280-210c-0135-62c5-0ac514e14162" />
          <code code="CONC" codeSystem="2.16.840.1.113883.5.6" displayName="Concern" />
          <!--<code code="282291009" displayName="diagnosis" codeSystem="2.16.840.1.113883.6.96" codeSystemName="SNOMED-CT"></code>-->
          <text>
            <xsl:value-of select="problemNameDisplayName"/>
          </text>
          <statusCode code="active" />
          <effectiveTime>
            <low>
              <xsl:if test="topLevelEffectiveTimeLow != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="topLevelEffectiveTimeLow"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="topLevelEffectiveTimeLow = '' or boolean(topLevelEffectiveTimeLow) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </low>
            <high>
              <xsl:if test="topLevelEffectiveTimeHigh != ''">
                <xsl:attribute name="value">
                  <xsl:value-of select="topLevelEffectiveTimeHigh"/>
                </xsl:attribute>
              </xsl:if>
              <xsl:if test="topLevelEffectiveTimeHigh = '' or boolean(topLevelEffectiveTimeHigh) = false">
                <xsl:attribute name="nullFlavor">
                  <xsl:text>UNK</xsl:text>
                </xsl:attribute>
              </xsl:if>
            </high>
          </effectiveTime>

          <entryRelationship typeCode="SUBJ">
            <observation classCode="OBS" moodCode="EVN">
              <!-- Conforms to C-CDA R2.1 Problem Observation (V3) -->
              <templateId root="2.16.840.1.113883.10.20.22.4.4" extension="2015-08-01" />
              <!-- Diagnosis template -->
              <templateId root="2.16.840.1.113883.10.20.24.3.135" />
              <id root="1.3.6.1.4.1.115" >
                <xsl:attribute name="extension">
                  <xsl:value-of select="id"/>
                </xsl:attribute>
              </id>
              <!--<id>
                <xsl:attribute name="root">
                  -->
              <!--<xsl:value-of select="generate-id(id)"/>-->
              <!--
                  <xsl:text>cbde95d0-d9dd-0132-854b-22000b549a64</xsl:text>
                </xsl:attribute>
              </id>-->
              <code code="29308-4" codeSystem="2.16.840.1.113883.6.1">
                <translation code="282291009" codeSystem="2.16.840.1.113883.6.96" />
              </code>
              <statusCode code="completed" />
              <effectiveTime>
                <low>
                  <xsl:if test="topLevelEffectiveTimeLow != ''">
                    <xsl:attribute name="value">
                      <xsl:value-of select="topLevelEffectiveTimeLow"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="topLevelEffectiveTimeLow = '' or boolean(topLevelEffectiveTimeLow) = false">
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </low>
                <high>
                  <xsl:if test="topLevelEffectiveTimeHigh != ''">
                    <xsl:attribute name="value">
                      <xsl:value-of select="topLevelEffectiveTimeHigh"/>
                    </xsl:attribute>
                  </xsl:if>
                  <xsl:if test="topLevelEffectiveTimeHigh = '' or boolean(topLevelEffectiveTimeHigh) = false">
                    <xsl:attribute name="nullFlavor">
                      <xsl:text>UNK</xsl:text>
                    </xsl:attribute>
                  </xsl:if>
                </high>
              </effectiveTime>


              <value xsi:type="CD">
                <xsl:attribute name="code">
                  <xsl:value-of select="problemNameCode"/>
                </xsl:attribute>
                <xsl:choose>
                  <xsl:when test="boolean(conceptCodeOID) and (conceptCodeOID != '')">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="conceptCodeOID"/>
                    </xsl:attribute>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.96</xsl:text>
                    </xsl:attribute>
                  </xsl:otherwise>
                </xsl:choose>
                <xsl:if test="boolean(conceptValueOID) and (conceptValueOID != '')">
                  <xsl:attribute name="sdtc:valueSet">
                    <xsl:value-of select="conceptValueOID"/>
                  </xsl:attribute>
                </xsl:if>
                <originalText>
                  <xsl:value-of select="problemNameDisplayName"/>
                </originalText>
              </value>
              <xsl:choose>
                <xsl:when test="targetSiteCode != ''">
                  <targetSiteCode>
                    <xsl:attribute name="code">
                      <xsl:value-of select="targetSiteCode"/>
                    </xsl:attribute>
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="targetSitecodeSystem"/>
                    </xsl:attribute>
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="targetSitecodevalueSet"/>
                    </xsl:attribute>
                  </targetSiteCode>
                </xsl:when>
                <xsl:otherwise>
                </xsl:otherwise>
              </xsl:choose>
            </observation>
          </entryRelationship>
        </act>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="Encounter">
    <xsl:for-each select="/QRDA/encounterListObj/Encounter">
      <entry>
        <act classCode="ACT" moodCode="EVN">
          <!--Encounter performed Act -->
          <templateId extension="2017-08-01" root="2.16.840.1.113883.10.20.24.3.133"/>
          <id extension="5c4dba388f590e04a0da26a7" root="1.3.6.1.4.1.115"/>
          <code code="ENC" codeSystem="2.16.840.1.113883.5.6" codeSystemName="ActClass" displayName="Encounter"/>
          <entryRelationship typeCode="SUBJ">
            <encounter classCode="ENC" moodCode="EVN">
              <!--  Encounter activities template -->
              <templateId extension="2015-08-01" root="2.16.840.1.113883.10.20.22.4.49"/>
              <!-- Encounter performed template -->
              <templateId extension="2017-08-01" root="2.16.840.1.113883.10.20.24.3.23"/>
              <id root="1.3.6.1.4.1.115" >
                <xsl:attribute name="extension">
                  <xsl:value-of select="visitID"/>
                </xsl:attribute>
              </id>


              <code>
                <xsl:attribute name="code">
                  <xsl:value-of select="cptCodes" />
                </xsl:attribute>

                <!--<xsl:attribute name="codeSystem">
                  <xsl:text>2.16.840.1.113883.6.12</xsl:text>
                </xsl:attribute>-->

                <xsl:choose>
                  <xsl:when test="conceptCodeOID != ''">
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="conceptCodeOID" />
                    </xsl:attribute>
                  </xsl:when>
                  <xsl:otherwise>
                    <xsl:attribute name="codeSystem">
                      <xsl:text>2.16.840.1.113883.6.12</xsl:text>
                    </xsl:attribute>
                  </xsl:otherwise>
                </xsl:choose>

                <xsl:if test="boolean(conceptValueOID) and (conceptValueOID != '')">
                  <xsl:attribute name="sdtc:valueSet">
                    <xsl:value-of select="conceptValueOID" />
                  </xsl:attribute>
                </xsl:if>

                <originalText>
                  <xsl:value-of select="text"/>
                </originalText>
              </code>

              <!--<code>
                <xsl:attribute name="code">
                  <xsl:value-of select="code"/>
                </xsl:attribute>
                <xsl:if test="CodeSystem != ''">
                  <xsl:attribute name="codeSystem">
                    <xsl:value-of select="CodeSystem"/>
                  </xsl:attribute>
                </xsl:if>
                <xsl:if test="CodeSystem = '' or boolean(CodeSystem) = false">
                  <xsl:attribute name="codeSystem">
                    <xsl:text>2.16.840.1.113883.6.12</xsl:text>
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

              <!--<code>
                <xsl:attribute name="code">
                  <xsl:text>99201</xsl:text>
                </xsl:attribute>
                <xsl:attribute name="codeSystem">
                  <xsl:text>2.16.840.1.113883.6.12</xsl:text>
                </xsl:attribute>                
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

              <xsl:choose>
                <xsl:when test="principaldiagnosiscode != ''">
                  <entryRelationship typeCode="REFR">
                    <observation classCode="OBS" moodCode="EVN">
                      <code code="8319008" codeSystem="2.16.840.1.113883.6.96" displayName="Principal Diagnosis" codeSystemName="SNOMED CT"/>
                      <value xsi:type="CD">
                        <xsl:attribute name="code">
                          <xsl:value-of select="principaldiagnosiscode"/>
                        </xsl:attribute>
                        <xsl:attribute name="codeSystem">
                          <xsl:value-of select="principaldiagnosiscodeSystem"/>
                        </xsl:attribute>
                        <xsl:attribute name="sdtc:valueSet">
                          <xsl:value-of select="principaldiagnosisvalueSet"/>
                        </xsl:attribute>
                      </value>
                    </observation>
                  </entryRelationship>
                </xsl:when>
                <xsl:otherwise>
                </xsl:otherwise>
              </xsl:choose>

              <participant typeCode="LOC">
                <!-- Facility Location template -->
                <templateId root="2.16.840.1.113883.10.20.24.3.100"/>
                <time>
                  <!-- Attribute: facility location arrival datetime -->
                  <low nullFlavor='UNK'/>
                  <!-- Attribute: facility location departure datetime -->
                  <high nullFlavor='UNK'/>
                </time>
                <participantRole classCode="SDLOC">
                  <code code="255327002"
                    codeSystem="2.16.840.1.113883.6.96" sdtc:valueSet="2.16.840.1.113883.3.464.1003.122.12.1003"/>
                  <telecom nullFlavor="UNK"/>
                  <playingEntity classCode="PLC">
                    <name>Ambulatory</name>
                  </playingEntity>
                </participantRole>
              </participant>

              <!--<xsl:choose>
                <xsl:when test="facilitylocationcode != ''">
                  <participant typeCode="LOC">
                    <templateId root="2.16.840.1.113883.10.20.24.3.100"/>
                    <time>
                      <low nullFlavor='UNK'/>
                      <high nullFlavor='UNK'/>
                    </time>
                    <participantRole classCode="SDLOC">
                      <code code="255327002" codeSystem="2.16.840.1.113883.6.96" sdtc:valueSet="2.16.840.1.113883.3.464.1003.122.12.1003">
                        <xsl:attribute name="code">
                          <xsl:value-of select="facilitylocationcode"/>
                        </xsl:attribute>
                        <xsl:attribute name="codeSystem">
                          <xsl:value-of select="facilitylocationcodesystem"/>
                        </xsl:attribute>
                        <xsl:attribute name="sdtc:valueSet">
                          <xsl:value-of select="facilitylocationvalueset"/>
                        </xsl:attribute>
                      </code>
                      <telecom nullFlavor="UNK"/>
                      <playingEntity classCode="PLC">
                        <name>Ambulatory</name>
                      </playingEntity>
                    </participantRole>
                  </participant>
                </xsl:when>
                <xsl:otherwise>
                </xsl:otherwise>
              </xsl:choose>-->


              <xsl:choose>
                <xsl:when test="dischargecode != ''">

                  <sdtc:dischargeDispositionCode>
                    <xsl:attribute name="code">
                      <xsl:value-of select="dischargecode"/>
                    </xsl:attribute>
                    <xsl:attribute name="codeSystem">
                      <xsl:value-of select="dischargecodeSystem"/>
                    </xsl:attribute>
                    <xsl:attribute name="sdtc:valueSet">
                      <xsl:value-of select="dischargevalueSet"/>
                    </xsl:attribute>
                  </sdtc:dischargeDispositionCode>

                </xsl:when>
                <xsl:otherwise>
                </xsl:otherwise>
              </xsl:choose>

            </encounter>
          </entryRelationship>
        </act>
      </entry>
    </xsl:for-each>
  </xsl:template>
  <xsl:template name="MedicationAdministered">
    <xsl:for-each select="/QRDA/immunizationListObj/Immunization">
      <entry>
        <act classCode="ACT" moodCode="EVN" >

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <!-- Medication, Administered template -->
          <!--<templateId root="2.16.840.1.113883.10.20.24.3.42"/>-->
          <templateId root="2.16.840.1.113883.10.20.24.3.140"/>
          <id root="1.3.6.1.4.1.115" >
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
        <substanceAdministration classCode="SBADM" moodCode="RQO" >

          <xsl:if test="negationInd != ''">
            <xsl:attribute name="negationInd">
              <xsl:value-of select="negationInd"/>
            </xsl:attribute>
          </xsl:if>

          <templateId root="2.16.840.1.113883.10.20.22.4.42" extension="2014-06-09" />
          <!-- Medication, Order template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.47" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115" >
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
        <act classCode="ACT" moodCode="EVN" >
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
              <id root="1.3.6.1.4.1.115" >
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
        <substanceAdministration classCode="SBADM" moodCode="EVN" >
          <!-- Medication Activity (consolidation) template -->
          <templateId root="2.16.840.1.113883.10.20.22.4.16" extension="2014-06-09" />
          <!-- Medication, Active template -->
          <templateId root="2.16.840.1.113883.10.20.24.3.41" extension="2016-02-01" />
          <id root="1.3.6.1.4.1.115" >
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
          <id root="1.3.6.1.4.1.115" >
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
            <value xsi:type="PQ" >
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
            <value xsi:type="PQ" >
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
        <!-- This is the templateId for Measure Section -->
        <templateId root="2.16.840.1.113883.10.20.24.2.2"/>
        <!-- This is the templateId for Measure Section QDM -->
        <templateId root="2.16.840.1.113883.10.20.24.2.3"/>
        <!-- This is the LOINC code for "Measure document". This stays the same for all measure section required by QRDA standard -->
        <code code="55186-1" codeSystem="2.16.840.1.113883.6.1"/>
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
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-5118-2F4E-0151-20A31A780368"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-5118-2F4E-0151-20A31A780368"/>
                    <!--CMS69:SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Body Mass Index (BMI) Screening and Follow-Up Plan</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="9A031BB8-3D9B-11E1-8634-00237D5BF174"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '68'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id extension="5c8450f0-046a-0137-a70a-0a8bbc4b405e" root="1.3.6.1.4.1.115"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id extension="40280382-5FA6-FE85-0160-0EA3E0012376" root="2.16.840.1.113883.4.738"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Percentage of visits for patients aged 18 years and older for which the eligible professional or eligible clinician attests to documenting a list of current medications using all immediate resources available on the date of the encounter. This list must include ALL known prescriptions, over-the-counters, herbals, and vitamin/mineral/dietary (nutritional) supplements AND must contain the medications&#39; name, dosage, frequency and route of administration.</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="9A032D9C-3D9B-11E1-8634-00237D5BF174"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '65'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-227C2F851589"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-227C2F851589"/>
                    <!--CMS65 SHOULD This is the title of the eMeasure -->
                    <text>Hypertension: Improvement in Blood Pressure</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="1D8363CE-A529-490B-8C98-9B54AA75DA06"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="6"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '50'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-5118-2F4E-0151-59FB81BF1055"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-5118-2F4E-0151-59FB81BF1055"/>
                    <!--CMS50 SHOULD This is the title of the eMeasure -->
                    <text>Closing the Referral Loop: Receipt of Specialist Report</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="F58FC0D6-EDF5-416A-8D29-79AFBFD24DEA"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '22'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-528A-60FF-0152-94967C8A0860"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-528A-60FF-0152-94967C8A0860"/>
                    <!--CMS22 SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Screening for High Blood Pressure and Follow-Up Documented</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="9A033A94-3D9B-11E1-8634-00237D5BF174"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '167'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A4838B80B79"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A4838B80B79"/>
                    <!--CMS167 SHOULD This is the title of the eMeasure -->
                    <text>Diabetic Retinopathy: Documentation of Presence or Absence of Macular Edema and Level of Severity of Retinopathy</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="50164228-9D64-4EFC-AF67-DA0547FF61F1"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '165'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-22B98CFF181A"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-22B98CFF181A"/>
                    <!--CMS165 SHOULD This is the title of the eMeasure -->
                    <text>Controlling High Blood Pressure</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="ABDC37CC-BAC6-4156-9B91-D1BE2C8B7268"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '143'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A3471E70B34"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A3471E70B34"/>
                    <!--CMS143 SHOULD This is the title of the eMeasure -->
                    <text>Primary Open-Angle Glaucoma (POAG): Optic Nerve Evaluation</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="DB9D9F09-6B6A-4749-A8B2-8C1FDB018823"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '142'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A31050D0B24"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A31050D0B24"/>
                    <!--CMS142 SHOULD This is the title of the eMeasure -->
                    <text>Diabetic Retinopathy: Communication with the Physician Managing Ongoing Diabetes Care</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="53D6D7C3-43FB-4D24-8099-17E74C022C05"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '138'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-503F-A1FC-0150-D33F5B0A1B8C"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-503F-A1FC-0150-D33F5B0A1B8C"/>
                    <!--CMS138 SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Tobacco Use: Screening and Cessation Intervention</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="E35791DF-5B25-41BB-B260-673337BC44A8"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '133'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1F44D4980F0F"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1F44D4980F0F"/>
                    <!--CMS133 SHOULD This is the title of the eMeasure -->
                    <text>CMS133:Cataracts: 20/40 or Better Visual Acuity within 90 Days Following Cataract Surgery</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="39E0424A-1727-4629-89E2-C46C2FBB3F5F"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '132'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A2308830B04"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A2308830B04"/>
                    <!--CMS132 SHOULD This is the title of the eMeasure -->
                    <text>Cataracts: Complications within 30 Days Following Cataract Surgery Requiring Additional Surgical Procedures</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="9A0339C2-3D9B-11E1-8634-00237D5BF174"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '131'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-22A24CDD1740"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-22A24CDD1740"/>
                    <!--CMS131 SHOULD This is the title of the eMeasure -->
                    <text>Diabetes: Eye Exam</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="D90BDAB4-B9D2-4329-9993-5C34E2C0DC66"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '122'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-229AFFF616EE"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-229AFFF616EE"/>
                    <!--CMS122 SHOULD This is the title of the eMeasure -->
                    <text>Diabetes: Hemoglobin A1c (HbA1c) Poor Control (&gt; 9%)</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="F2986519-5A4E-4149-A8F2-AF0A1DC7F6BC"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <!--liquid-->
          <xsl:when test="/QRDA/CQMNumber = '2'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280382-5B4D-EEBC-015B-5844953B00A3"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280382-5B4D-EEBC-015B-5844953B00A3"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Screening for Depression and Follow-Up Plan</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="9A031E24-3D9B-11E1-8634-00237D5BF174"/>
                  </externalDocument>
                </reference>
              </organizer>
            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '117'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A4BA57F0B8A"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A4BA57F0B8A"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Childhood Immunization Status</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="B2802B7A-3580-4BE8-9458-921AEA62B78C"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '126'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A6115C60BEC"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A6115C60BEC"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Use of Appropriate Medications for Asthma</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="59E84144-6332-4369-AEBD-03A7899CA3DA"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
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
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-22A639D81762"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-22A639D81762"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>ADHD: Follow-Up Care for Children Prescribed Attention-Deficit/Hyperactivity Disorder (ADHD) Medication</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="703CC49B-B653-4885-80E8-245A057F5AE9"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="6"/>
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
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-22B695B217DC"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-22B695B217DC"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Weight Assessment and Counseling for Nutrition and Physical Activity for Children and Adolescents</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="0B63F730-25D6-4248-B11F-8C09C66A04EB"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
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
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-56D2B4F01AE5"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-56D2B4F01AE5"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Use of High-Risk Medications in the Elderly</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="A3837FF8-1ABC-4BA9-800E-FD4E7953ADBD"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '147'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-395CE63513AF"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-395CE63513AF"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Preventive Care and Screening: Influenza Immunization</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="A244AA29-7D11-4616-888A-86E376BFCC6F"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="6"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '130'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-22A1E7E81737"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-22A1E7E81737"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Colorectal Cancer Screening</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="AA2A4BBC-864F-45EE-B17A-7EBCC62E6AAC"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '127'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A646A2A0BFA"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A646A2A0BFA"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Pneumococcal Vaccination Status for Older Adults</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="59657B9B-01BF-4979-A090-8534DA1D0516"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '125'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-229C4EA3170C"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-229C4EA3170C"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Breast Cancer Screening</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="19783C1B-4FD1-46C1-8A96-A2F192B97EE0"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '124'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-51F0-825B-0152-229BDCAB1702"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-51F0-825B-0152-229BDCAB1702"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Cervical Cancer Screening</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="42E7E489-790F-427A-A1A6-D6E807F65A6D"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '157'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-52FC-3A32-0153-1A4425A90B6C"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-52FC-3A32-0153-1A4425A90B6C"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Oncology: Medical and Radiation - Pain Intensity Quantified</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="9A0330D0-3D9B-11E1-8634-00237D5BF174"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="5"/>
                  </externalDocument>
                </reference>
              </organizer>

            </entry>
          </xsl:when>
          <xsl:when test="/QRDA/CQMNumber = '129'">
            <entry>
              <organizer classCode="CLUSTER" moodCode="EVN">
                <!-- This is the templateId for Measure Reference -->
                <templateId root="2.16.840.1.113883.10.20.24.3.98"/>
                <!-- This is the templateId for eMeasure Reference QDM -->
                <templateId root="2.16.840.1.113883.10.20.24.3.97"/>
                <id root="1.3.6.1.4.1.115" extension="40280381-503F-A1FC-0151-10DE35992766"/>
                <statusCode code="completed"/>
                <!-- Containing isBranch external references -->
                <reference typeCode="REFR">
                  <externalDocument classCode="DOC" moodCode="EVN">
                    <!-- SHALL: This is the version specific identifier for eMeasure: QualityMeasureDocument/id it is a GUID-->
                    <id root="2.16.840.1.113883.4.738" extension="40280381-503F-A1FC-0151-10DE35992766"/>
                    <!-- SHOULD This is the title of the eMeasure -->
                    <text>Prostate Cancer: Avoidance of Overuse of Bone Scan for Staging Low Risk Prostate Cancer Patients</text>
                    <!-- SHOULD: setId is the eMeasure version neutral id  -->
                    <setId root="1635C14D-E612-4FA6-96CD-285361AA7F7B"/>
                    <!-- This is the sequential eMeasure Version number -->
                    <versionNumber value="6"/>
                  </externalDocument>
                </reference>
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
            <id root="2.16.840.1.113883.4.6" >
              <xsl:attribute name="extension">
                <xsl:value-of select="/QRDA/authorObj/NPI"/>
              </xsl:attribute>
            </id>
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
              <!-- This is the organization TIN -->
              <id root="2.16.840.1.113883.4.2" >
                <xsl:attribute name="extension">
                  <xsl:value-of select="/QRDA/authorObj/NPI"/>
                </xsl:attribute>
              </id>
              <!-- This is the organization CCN -->
              <!--<id root="2.16.840.1.113883.4.336">
                <xsl:attribute name="extension">
                  <xsl:value-of select="/QRDA/authorObj/CCN"/>
                </xsl:attribute>
              </id>-->
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
          <telecom use="WP" >
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
            <telecom use="WP" >
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
        <time value="20131028" />
        <assignedAuthor>
          <id root="2.16.840.1.113883.4.6" assigningAuthorityName="NPI" >
            <xsl:attribute name="extension">
              <xsl:value-of select="NPI"/>
            </xsl:attribute>
          </id>
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
          <telecom use="WP" >
            <xsl:attribute name="value">
              <xsl:value-of select="//custodianObj/phone"/>
            </xsl:attribute>
          </telecom>
          <assignedAuthoringDevice>
            <manufacturerModelName>Test</manufacturerModelName >
            <softwareName>Test</softwareName >
          </assignedAuthoringDevice >
        </assignedAuthor>
      </author>
    </xsl:for-each>

  </xsl:template>
  <xsl:template name="patientRoleObj">
    <recordTarget>
      <xsl:for-each select="/QRDA/patientRoleObj">
        <patientRole>
          <id root="2.16.840.1.113883.4.572">
            <xsl:attribute name="extension">
              <xsl:value-of select="mrn"></xsl:value-of>
            </xsl:attribute>
          </id>
          <addr use="HP">
            <streetAddressLine>
              <xsl:value-of select="patientAddress/streetAddressLine"/>
            </streetAddressLine>
            <city>
              <xsl:value-of select="patientAddress/city"/>
            </city>
            <state>
              <xsl:value-of select="patientAddress/state"/>
            </state>
            <postalCode>
              <xsl:value-of select="patientAddress/postalCode"/>
            </postalCode>
            <country>
              <xsl:value-of select="patientAddress/country"/>
            </country>
          </addr>
          <telecom use="WP">
            <xsl:attribute name="value">
              <xsl:value-of select="patientAddress/phone"/>
            </xsl:attribute>
          </telecom>
          <patient>
            <name>
              <given>
                <xsl:value-of select="patientFirstName"/>
              </given>
              <family>
                <xsl:value-of select="patientFamilyName"/>
              </family>
            </name>
            <administrativeGenderCode codeSystem="2.16.840.1.113883.5.1" codeSystemName="HL7 AdministrativeGender">
              <xsl:attribute name="code">
                <xsl:value-of select="administrativeGenderCode"/>
              </xsl:attribute>
            </administrativeGenderCode>
            <birthTime>
              <xsl:attribute name="value">
                <xsl:value-of select="birthTime"/>
              </xsl:attribute>
            </birthTime>
            <raceCode codeSystemName="CDC Race and Ethnicity" codeSystem="2.16.840.1.113883.6.238">
              <xsl:attribute name="code">
                <xsl:value-of select="raceCode"/>
              </xsl:attribute>
              <xsl:attribute name="displayName">
                <xsl:value-of select="race"/>
              </xsl:attribute>
            </raceCode>
            <ethnicGroupCode codeSystemName="CDC Race and Ethnicity" codeSystem="2.16.840.1.113883.6.238">
              <xsl:attribute name="code">
                <xsl:value-of select="ethnicGroupCode"/>
              </xsl:attribute>
              <xsl:attribute name="displayName">
                <xsl:value-of select="ethnicGroupCodeDisplayName"/>
              </xsl:attribute>
            </ethnicGroupCode>
            <languageCommunication>
              <templateId root="2.16.840.1.113883.3.88.11.83.2" assigningAuthorityName="HITSP/C83"/>
              <templateId root="1.3.6.1.4.1.19376.1.5.3.1.2.1" assigningAuthorityName="IHE/PCC"/>
              <languageCode>
                <xsl:attribute name="code">
                  <xsl:value-of select="languageCommunication"/>
                </xsl:attribute>
              </languageCode>
            </languageCommunication>
          </patient>
        </patientRole>
      </xsl:for-each>
    </recordTarget>
  </xsl:template>
</xsl:stylesheet>
