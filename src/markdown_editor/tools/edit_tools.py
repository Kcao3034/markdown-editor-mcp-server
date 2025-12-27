import logging
import os
from typing import Dict, Any, List, Optional
from ..core.document import Document

logger = logging.getLogger(__name__)

class EditTool:
    """Tool for working with document content"""
    
    def __init__(self):
        self._documents: Dict[str, Document] = {}

    def get_doc(self, file_path: str) -> Document:
        """Get or load document by path"""
        abs_path = os.path.abspath(file_path)
        if abs_path not in self._documents:
            if os.path.exists(abs_path):
                with open(abs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._documents[abs_path] = Document(content=content)
            else:
                self._documents[abs_path] = Document(content="")
        return self._documents[abs_path]

    async def get_structure(self, file_path: str, depth: Optional[int] = None) -> List[dict]:
        doc = self.get_doc(file_path)
        return doc.get_structure(depth=depth)

    async def read(self, file_path: str, path: str) -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        return doc.view_element(path)

    async def replace(self, file_path: str, path: str, new_content: str) -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        result = doc.replace(path, new_content)
        if "success" in result:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.get_content())
        return result

    async def insert(self, file_path: str, path: str, element_type: str, content: str, 
                    where: str = "after", heading_level: int = 1) -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        if where == "before":
            result = doc.insert_before(path, element_type, content, heading_level)
        else:
            result = doc.insert_after(path, element_type, content, heading_level)
        if "success" in result:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.get_content())
        return result

    async def delete(self, file_path: str, path: str) -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        result = doc.delete(path)
        if "success" in result:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.get_content())
        return result

    async def undo(self, file_path: str, count: int = 1) -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        result = doc.undo(count)
        if "success" in result:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.get_content())
        return result

    async def search(self, file_path: str, query: str) -> List[Dict[str, Any]]:
        doc = self.get_doc(file_path)
        return doc.search_text(query)

    async def get_context(self, file_path: str, path: str) -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        return doc.get_context(path)

    async def move(self, file_path: str, src_path: str, dst_path: str, where: str = "after") -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        result = doc.move_element(src_path, dst_path, where)
        if "success" in result:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.get_content())
        return result

    async def update_metadata(self, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        doc = self.get_doc(file_path)
        result = doc.update_metadata(metadata)
        if "success" in result:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc.get_content())
        return result

# Global instance following the template
_instance = EditTool()

# Async wrappers following the template
async def get_document_structure(file_path: str, depth: Optional[int] = None):
    return await _instance.get_structure(file_path, depth)

async def read_element(file_path: str, path: str):
    return await _instance.read(file_path, path)

async def replace_content(file_path: str, path: str, new_content: str):
    return await _instance.replace(file_path, path, new_content)

async def insert_element(file_path: str, path: str, element_type: str, content: str, 
                         where: str = "after", heading_level: int = 1):
    return await _instance.insert(file_path, path, element_type, content, where, heading_level)

async def delete_element(file_path: str, path: str):
    return await _instance.delete(file_path, path)

async def undo_changes(file_path: str, count: int = 1):
    return await _instance.undo(file_path, count)

async def search_in_document(file_path: str, query: str):
    return await _instance.search(file_path, query)

async def get_element_context(file_path: str, path: str):
    return await _instance.get_context(file_path, path)

async def move_document_element(file_path: str, src_path: str, dst_path: str, where: str = "after"):
    return await _instance.move(file_path, src_path, dst_path, where)

async def update_document_metadata(file_path: str, metadata: Dict[str, Any]):
    return await _instance.update_metadata(file_path, metadata)
