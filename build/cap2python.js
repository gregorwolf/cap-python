/*
Generated using ChatGPT with the following prompt:

Please create the needed JavaScript code that can run in Node.JS using the following JSON:

```json
{
  "namespace": "my.bookshop",
  "definitions": {
    "my.bookshop.Books": {
      "kind": "entity",
      "elements": {
        "ID": {
          "key": true,
          "type": "cds.Integer"
        },
        "title": {
          "type": "cds.String"
        },
        "stock": {
          "type": "cds.Integer"
        }
      }
    },
    "CatalogService": {
      "@source": "srv/cat-service.cds",
      "kind": "service",
      "@requires": "authenticated-user"
    },
    "CatalogService.Books": {
      "kind": "entity",
      "@readonly": true,
      "projection": {
        "from": {
          "ref": [
            "my.bookshop.Books"
          ]
        }
      },
      "elements": {
        "ID": {
          "key": true,
          "type": "cds.Integer"
        },
        "title": {
          "type": "cds.String"
        },
        "stock": {
          "type": "cds.Integer"
        }
      }
    }
  },
  "meta": {
    "creator": "CDS Compiler v4.9.4",
    "flavor": "inferred"
  },
  "$version": "2.0"
}
```

and translate all elements of kind entity into a Python class from the pydantic BaseModel following this example:


```Python
class Books(BaseModel):
    ID: int
    title: str
    stock: int
```
*/
const fs = require('fs');

// Read the JSON file
const jsonData = JSON.parse(fs.readFileSync('gen/srv/srv/csn.json', 'utf8'));

// Function to map CDS types to Python types
function mapCdsTypeToPythonType(cdsType) {
  switch (cdsType) {
    case 'cds.Integer':
      return 'int';
    case 'cds.String':
      return 'str';
    // Add more mappings as needed
    default:
      return 'Any'; // Use Any for unrecognized types
  }
}

// Function to generate Python classes from JSON
function generatePythonClasses(definitions) {
  let pythonClasses = '';

  for (const [name, definition] of Object.entries(definitions)) {
    if (definition.kind === 'entity' && !definition.projection) {
      const className = name.split('.').pop(); // Get the class name without namespace
      pythonClasses += `class ${className}(BaseModel):\n`;

      for (const [elementName, elementDefinition] of Object.entries(definition.elements)) {
        const pythonType = mapCdsTypeToPythonType(elementDefinition.type);
        pythonClasses += `    ${elementName}: ${pythonType}\n`;
      }

      pythonClasses += '\n';
    }
  }

  return pythonClasses;
}

// Generate the Python classes
const pythonClasses = generatePythonClasses(jsonData.definitions);

// Add import statement for pydantic
const pythonCode = `from pydantic import BaseModel\n\n${pythonClasses}`;

// Save the Python code to a file
fs.writeFileSync('gen/models.py', pythonCode);

console.log('Python classes generated and saved to models.py');
